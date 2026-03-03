#!/usr/bin/env python3
import json
import sys
from decimal import Decimal, ROUND_DOWN, getcontext
from pathlib import Path


getcontext().prec = 50
VECTOR_DIR = Path("docs/test-vectors")
EPS = Decimal("0.000000001")


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def d(value: object) -> Decimal:
    return Decimal(str(value))


def floor_to_decimals(value: Decimal, decimals: int) -> Decimal:
    quantum = Decimal("1").scaleb(-decimals)
    return value.quantize(quantum, rounding=ROUND_DOWN)


def numeric_like(value: object) -> bool:
    if isinstance(value, (int, float, Decimal)):
        return True
    if isinstance(value, str):
        try:
            Decimal(value)
            return True
        except Exception:
            return False
    return False


def assert_value(path: str, actual: object, expected: object) -> None:
    if numeric_like(expected):
        actual_d = d(actual)
        expected_d = d(expected)
        if abs(actual_d - expected_d) > EPS:
            fail(f"{path}: expected {expected_d}, got {actual_d}")
        return

    if str(actual) != str(expected):
        fail(f"{path}: expected {expected!r}, got {actual!r}")


def run_settlement_vector(vector: dict) -> None:
    inputs = vector["inputs"]
    expected = vector["expected"]

    oracle_age = int(inputs["oracle_age_seconds"])
    oracle_max_age = int(inputs["oracle_max_age_seconds"])
    settlement_state = "HALT" if oracle_age > oracle_max_age else "OK"

    nodes = inputs["nodes"]
    results: dict[str, dict[str, object]] = {}

    cdn_rate = d(inputs["cdn_rate_usd_per_tb"])
    st_rate = d(inputs["storage_rate_usd_per_tb_month"])
    pipe_price = d(inputs["oracle_price_usd_per_pipe"])

    if pipe_price <= 0:
        fail(f"{vector['name']}: oracle_price_usd_per_pipe must be > 0")

    bw_cap_pct = d(inputs["bw_bucket_cap_pct"])
    st_cap_pct = d(inputs["st_bucket_cap_pct"])
    e_cap_month = d(inputs["e_cap_month_pipe"])
    staking_commission_bps = d(inputs["staking_commission_bps"])
    pipe_decimals = int(inputs["pipe_decimals"])

    b_raw = Decimal("0")
    s_raw = Decimal("0")

    for node in nodes:
        node_id = str(node["id"])
        q_i = int(node["q"])
        s_i = int(node["s"])
        w_i = int(node["w"])
        e_i = q_i * s_i * w_i

        bw_tb = d(node["bw_tb"])
        st_tbm = d(node["st_tbm"])

        if settlement_state == "HALT":
            cdn_usd_i = Decimal("0")
            st_usd_i = Decimal("0")
            cdn_raw_pipe_i = Decimal("0")
            st_raw_pipe_i = Decimal("0")
        else:
            cdn_usd_i = bw_tb * cdn_rate * d(e_i)
            st_usd_i = st_tbm * st_rate * d(e_i)
            cdn_raw_pipe_i = cdn_usd_i / pipe_price
            st_raw_pipe_i = st_usd_i / pipe_price
            b_raw += cdn_raw_pipe_i
            s_raw += st_raw_pipe_i

        results[node_id] = {
            "e": e_i,
            "cdn_usd": cdn_usd_i,
            "st_usd": st_usd_i,
            "cdn_raw_pipe": cdn_raw_pipe_i,
            "st_raw_pipe": st_raw_pipe_i,
            "gross_pipe": Decimal("0"),
            "net_pipe": Decimal("0"),
        }

    if settlement_state == "HALT":
        b_scale = Decimal("0")
        s_scale = Decimal("0")
    else:
        b_cap = (bw_cap_pct / Decimal("100")) * e_cap_month
        s_cap = (st_cap_pct / Decimal("100")) * e_cap_month
        b_scale = Decimal("0") if b_raw == 0 else min(Decimal("1"), b_cap / b_raw)
        s_scale = Decimal("0") if s_raw == 0 else min(Decimal("1"), s_cap / s_raw)

    commission_multiplier = Decimal("1") - (staking_commission_bps / Decimal("10000"))
    total_gross = Decimal("0")
    total_net = Decimal("0")

    for node_id, row in results.items():
        gross = (row["cdn_raw_pipe"] * b_scale) + (row["st_raw_pipe"] * s_scale)
        net = floor_to_decimals(gross * commission_multiplier, pipe_decimals)

        row["gross_pipe"] = gross
        row["net_pipe"] = net

        total_gross += gross
        total_net += net

    assert_value(f"{vector['name']}.settlement_state", settlement_state, expected["settlement_state"])
    assert_value(f"{vector['name']}.B_scale", b_scale, expected["B_scale"])
    assert_value(f"{vector['name']}.S_scale", s_scale, expected["S_scale"])

    for node_id, node_expected in expected["nodes"].items():
        if node_id not in results:
            fail(f"{vector['name']}: expected node `{node_id}` missing from results")
        node_actual = results[node_id]
        for key, expected_value in node_expected.items():
            if key not in node_actual:
                fail(f"{vector['name']}: unknown settlement field `{key}` in expected node `{node_id}`")
            assert_value(f"{vector['name']}.nodes.{node_id}.{key}", node_actual[key], expected_value)

    assert_value(f"{vector['name']}.totals.gross_pipe", total_gross, expected["totals"]["gross_pipe"])
    assert_value(f"{vector['name']}.totals.net_pipe", total_net, expected["totals"]["net_pipe"])


def compute_assignment_alloc(inputs: dict) -> tuple[dict[str, Decimal], Decimal]:
    stake_min = d(inputs["stake_min"])
    priority_stake_cap = d(inputs["priority_stake_cap"])
    max_queue_share = d(inputs["max_queue_share"])
    cluster_queue_share_cap = d(inputs["cluster_queue_share_cap"])
    new_node_queue_share_cap = d(inputs["new_node_queue_share_cap"])

    nodes = []
    for node in inputs["nodes"]:
        node_id = str(node["id"])
        eligible = int(node.get("eligible", 1))
        if not eligible:
            continue

        stake = d(node["stake"])
        if stake <= 0:
            continue

        cluster_id = str(node["cluster"])
        is_new = bool(node.get("is_new", False))

        weight = (stake / stake_min).sqrt()
        weight = min(priority_stake_cap, weight)
        if weight <= 0:
            continue

        node_cap = min(max_queue_share, new_node_queue_share_cap if is_new else Decimal("1"))
        nodes.append(
            {
                "id": node_id,
                "cluster": cluster_id,
                "weight": weight,
                "node_cap": node_cap,
            }
        )

    if not nodes:
        return {}, Decimal("1")

    explicit_cluster_caps: dict[str, Decimal] = {}
    for cluster_id, cap in inputs.get("cluster_caps", {}).items():
        explicit_cluster_caps[str(cluster_id)] = d(cap)

    cluster_caps: dict[str, Decimal] = {}
    for node in nodes:
        cluster_caps[node["cluster"]] = explicit_cluster_caps.get(node["cluster"], cluster_queue_share_cap)

    assigned: dict[str, Decimal] = {node["id"]: Decimal("0") for node in nodes}

    def cluster_total(cluster_id: str) -> Decimal:
        total = Decimal("0")
        for node in nodes:
            if node["cluster"] == cluster_id:
                total += assigned[node["id"]]
        return total

    remaining = Decimal("1")

    for _ in range(256):
        active = []
        for node in nodes:
            node_room = node["node_cap"] - assigned[node["id"]]
            cluster_room = cluster_caps[node["cluster"]] - cluster_total(node["cluster"])
            if node_room > EPS and cluster_room > EPS and node["weight"] > 0:
                active.append(node)

        if not active or remaining <= EPS:
            break

        total_weight = sum((node["weight"] for node in active), Decimal("0"))
        if total_weight <= 0:
            break

        alpha_target = remaining / total_weight

        alpha_node_cap = min(
            (node["node_cap"] - assigned[node["id"]]) / node["weight"] for node in active
        )

        cluster_weight: dict[str, Decimal] = {}
        for node in active:
            cluster_weight[node["cluster"]] = cluster_weight.get(node["cluster"], Decimal("0")) + node["weight"]

        alpha_cluster_cap = min(
            (cluster_caps[cluster_id] - cluster_total(cluster_id)) / weight_sum
            for cluster_id, weight_sum in cluster_weight.items()
            if weight_sum > 0
        )

        alpha = min(alpha_target, alpha_node_cap, alpha_cluster_cap)
        if alpha <= EPS:
            break

        delta = Decimal("0")
        for node in sorted(active, key=lambda item: item["id"]):
            node_id = node["id"]
            add = alpha * node["weight"]

            node_room = node["node_cap"] - assigned[node_id]
            cluster_room = cluster_caps[node["cluster"]] - cluster_total(node["cluster"])
            add = min(add, node_room, cluster_room)

            if add > 0:
                assigned[node_id] += add
                delta += add

        if delta <= EPS:
            break

        remaining -= delta

    if abs(remaining) <= EPS:
        remaining = Decimal("0")

    return assigned, remaining


def run_assignment_vector(vector: dict) -> None:
    inputs = vector["inputs"]
    expected = vector["expected"]

    assigned, unallocated = compute_assignment_alloc(inputs)

    for node_id, expected_share in expected.get("alloc_share", {}).items():
        actual_share = assigned.get(node_id, Decimal("0"))
        assert_value(f"{vector['name']}.alloc_share.{node_id}", actual_share, expected_share)

    for cluster_id, expected_total in expected.get("cluster_totals", {}).items():
        total = Decimal("0")
        for node in inputs["nodes"]:
            if str(node["cluster"]) == str(cluster_id):
                total += assigned.get(str(node["id"]), Decimal("0"))
        assert_value(f"{vector['name']}.cluster_totals.{cluster_id}", total, expected_total)

    if "unallocated_share" in expected:
        assert_value(f"{vector['name']}.unallocated_share", unallocated, expected["unallocated_share"])


def main() -> None:
    if not VECTOR_DIR.exists():
        fail(f"Missing test-vector directory: {VECTOR_DIR}")

    files = sorted(VECTOR_DIR.glob("*.json"))
    if not files:
        fail(f"No test vectors found in: {VECTOR_DIR}")

    for path in files:
        try:
            vector = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            fail(f"Invalid JSON in {path}: {e}")

        name = vector.get("name", path.stem)
        vector_type = vector.get("type")
        if not vector_type:
            fail(f"{path}: missing `type`")

        vector["name"] = str(name)

        if vector_type == "settlement":
            run_settlement_vector(vector)
        elif vector_type == "assignment":
            run_assignment_vector(vector)
        else:
            fail(f"{path}: unknown type `{vector_type}`")

    print(f"tokenomics-test-vectors-passed ({len(files)} vectors)")


if __name__ == "__main__":
    main()
