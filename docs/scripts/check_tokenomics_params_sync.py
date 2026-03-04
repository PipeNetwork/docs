#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


POLICY_PATH = Path("docs/Tokenomics.md")
SPEC_PATH = Path("docs/tokenomics-operations-spec.md")
PARAMS_JSON_PATH = Path("docs/tokenomics-params.json")
SECTION_HEADER = "## 7) Parameter Registry (Defaults)"


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def parse_tokenomics_version(md: str) -> str:
    m = re.search(r"^\|\s*Version\s*\|\s*([^\|]+?)\s*\|$", md, flags=re.MULTILINE)
    if not m:
        fail("Could not parse Tokenomics version from policy header table.")
    return m.group(1).strip()


def parse_parameter_table(md: str) -> list[dict[str, str]]:
    lines = md.splitlines()
    try:
        section_idx = next(i for i, line in enumerate(lines) if line.strip() == SECTION_HEADER)
    except StopIteration:
        fail(f"Could not find section header: {SECTION_HEADER}")

    header_idx = None
    for i in range(section_idx + 1, len(lines)):
        if lines[i].strip().startswith("| Parameter |"):
            header_idx = i
            break
    if header_idx is None:
        fail("Could not find parameter table header row.")

    headers = [c.strip() for c in lines[header_idx].strip().strip("|").split("|")]
    if headers != [
        "Parameter",
        "Current Value",
        "Unit",
        "Min",
        "Max",
        "Enforced Where",
        "Protocol-Updateable",
        "Change Effective Field",
        "Parameter Owner",
    ]:
        fail(f"Unexpected parameter table headers: {headers}")

    def norm_cell(value: str) -> str:
        v = value.strip()
        if len(v) >= 2 and v.startswith("`") and v.endswith("`"):
            v = v[1:-1].strip()
        return v

    rows: list[dict[str, str]] = []
    for i in range(header_idx + 2, len(lines)):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) != len(headers):
            fail(f"Malformed table row at line {i + 1}: {line}")
        row = {k: norm_cell(v) for k, v in dict(zip(headers, cols)).items()}
        rows.append(row)

    if not rows:
        fail("Parameter table is empty.")
    return rows


def load_json_params() -> tuple[str, list[dict[str, str]]]:
    try:
        data = json.loads(PARAMS_JSON_PATH.read_text())
    except FileNotFoundError:
        fail(f"Missing file: {PARAMS_JSON_PATH}")
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON in {PARAMS_JSON_PATH}: {e}")

    if "version" not in data or "parameters" not in data:
        fail("tokenomics-params.json must include `version` and `parameters`.")

    version = str(data["version"])
    params = data["parameters"]
    if not isinstance(params, list):
        fail("`parameters` must be a list.")

    normalized: list[dict[str, str]] = []
    for idx, p in enumerate(params):
        if not isinstance(p, dict):
            fail(f"Parameter at index {idx} must be an object.")
        normalized.append(
            {
                "Parameter": str(p.get("Parameter", "")),
                "Current Value": str(p.get("Current Value", "")),
                "Unit": str(p.get("Unit", "")),
                "Min": str(p.get("Min", "")),
                "Max": str(p.get("Max", "")),
                "Enforced Where": str(p.get("Enforced Where", "")),
                "Protocol-Updateable": str(p.get("Protocol-Updateable", "")),
                "Change Effective Field": str(p.get("Change Effective Field", "")),
                "Parameter Owner": str(p.get("Parameter Owner", "")),
            }
        )
    return version, normalized


def main() -> None:
    policy_md = POLICY_PATH.read_text()
    spec_md = SPEC_PATH.read_text()
    policy_version = parse_tokenomics_version(policy_md)
    spec_rows = parse_parameter_table(spec_md)
    json_version, json_rows = load_json_params()

    if policy_version != json_version:
        fail(
            f"Version mismatch: Tokenomics.md has `{policy_version}` but tokenomics-params.json has `{json_version}`."
        )

    if spec_rows != json_rows:
        print("ERROR: Parameter registry drift detected between markdown table and JSON.")
        print(f"Spec rows: {len(spec_rows)} | JSON rows: {len(json_rows)}")
        min_len = min(len(spec_rows), len(json_rows))
        for i in range(min_len):
            if spec_rows[i] != json_rows[i]:
                print(f"First mismatch at row {i + 1}:")
                print(f"  markdown: {spec_rows[i]}")
                print(f"  json:     {json_rows[i]}")
                sys.exit(1)
        if len(spec_rows) != len(json_rows):
            print("Row counts differ.")
            sys.exit(1)
        fail("Unknown parameter table mismatch.")

    print("tokenomics-params-sync-passed")


if __name__ == "__main__":
    main()
