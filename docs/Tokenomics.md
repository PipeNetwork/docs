# Pipe Network Tokenomics Policy (Mainnet Tokenomics 2.0)

## Policy Header

| Field | Value |
| --- | --- |
| Version | 2.6.0 |
| Effective Date | March 3, 2026 |
| Status | Active |
| Supersedes | Prior mainnet payout models with legacy boost programs, tiered scaling, soft gate enforcement, or no stake activation gate |

This document is the canonical reference for Mainnet economics and payout policy.

## 0) Source of Truth

- This document is the canonical, normative policy for Mainnet tokenomics.
- Secondary docs are operator summaries and onboarding aids.
- If any secondary doc conflicts with this document, this document wins.

## Policy Change Log

| Version | Date | Changes |
| --- | --- | --- |
| `2.6.0` | March 3, 2026 | Defined settlement vs Jito epoch terms, added parameter bounds and effective field semantics, replaced narrative examples with executable test vectors, and added reporting schema plus CI drift/link checks. |
| `2.5.0` | March 3, 2026 | Added source-of-truth rule, deterministic settlement spec, fail-closed controls, anti-sybil assignment caps, suspension state machine, machine-readable parameter mapping, and CI policy guardrails. |
| `2.4.0` | March 3, 2026 | Clarified LovePIPE unstake timing is epoch-based (not fixed 30-day) and aligned mainnet docs to that policy. |
| `2.3.0` | March 3, 2026 | Mainnet Tokenomics 2.0 rollout: flat-rate payouts, hard-fail eligibility, stake/wallet gates, and assignment-priority model. |

## 1) Scope

- Network: Mainnet
- Chain: Solana (SPL token)
- Token: PIPE
- Model: Proof-of-Useful-Work (PoUW) for CDN bandwidth and storage capacity

This document does not define storage bandwidth pricing.

### Epoch Terminology

- `settlement_epoch`: the monthly accounting and payout window used by this policy.
- `jito_epoch`: the slot-based epoch used by Jito restaking (currently observed at `432000` slots on mainnet; upstream-configurable).
- Unless explicitly stated otherwise, "epoch" in this policy means `settlement_epoch`.

## 2) Units, Metering, and Rounding

### Units

- `1 TB = 1,000,000,000,000 bytes` (decimal, not TiB)
- `1 TB-month = 1 TB held for a full calendar month settlement_epoch`

### Metering

- CDN bandwidth work counts successful edge egress bytes delivered to clients.
- Storage capacity work counts average stored bytes over the settlement_epoch.
- Storage capacity is prorated by time held in the settlement_epoch:

```text
storage_tb_month_i = (sum_over_settlement_epoch_days(avg_stored_bytes_i_day) / 1e12) / days_in_settlement_epoch
```

### Deterministic Settlement Specification

- Internal work accounting is byte-level and timestamped.
- Settlement arithmetic uses fixed-point decimal with at least 18 decimal places internally.
- Deterministic processing order:
  1. Compute `bw_tb_i` and `st_tbm_i` from metered bytes/time.
  2. Apply eligibility gate `e_i` (hard-fail).
  3. Compute USD values at fixed rates (`$0.25/TB`, `$0.25/TB-month`).
  4. Convert USD to raw PIPE using settlement_epoch oracle price `P`.
  5. Apply bucket scaling (`B_scale`, `S_scale`).
  6. Apply staking commission (`7%`) to get `net_pipe_i`.
  7. Round `net_pipe_i` down to `PIPE_DECIMALS = 6`.
- Rounding mode for settlement is floor (`round_down`) at final payout output only.
- Any residual below 1 micro-PIPE per node is carried into settlement_epoch residual accounting and published in reports.
- Tie-break rules where equal ordering is possible:
  - Node ordering uses ascending node identity public key bytes.
  - If equal stake priority weights in scheduling, assign using the same node-key sort order.

## 3) Transition to Tokenomics 2.0

| Topic | Previous Mainnet Draft | Tokenomics 2.0 |
| --- | --- | --- |
| CDN bandwidth base rate | $1.00/TB | $0.25/TB |
| Storage capacity base rate | $10.00/TB-month | $0.25/TB-month |
| Legacy whitelist boost program | Legacy boosted payouts | Removed |
| Eligibility model | Tiered payout scaling | Flat-rate payout with hard-fail quality + stake + wallet eligibility |
| Storage bandwidth pricing | Mixed references | Out of scope |

## 4) Supply and Genesis Allocation

Total supply at TGE: `1,000,000,000 PIPE`.

Allocation:

- Community: `22%` = `220,000,000`
- Strategic Investors: `32.34%` = `323,400,000`
- Core Contributors and Labs: `15.67%` = `156,700,000`
- Ecosystem and Treasury: `19.99%` = `199,900,000`
- Node Operators: `10%` = `100,000,000`

Unlock schedules are published at or before TGE.

## 5) Disinflation and Monthly Mint Cap

Annual nominal inflation cap:

```text
r_y = max(1.5%, 12% * 0.82^(y - 1))
```

Monthly cap in year `y`:

```text
E_cap_month = (r_y / 12) * S_year_start
```

- `S_year_start` is circulating supply at the start of the year.
- No catch-up: unused monthly capacity does not mint later.

## 6) Usage-Gated Emissions and Buckets

PIPE only mints after verifiable useful work.

- Bandwidth bucket cap: up to `25%` of `E_cap_month`
- Storage bucket cap: up to `25%` of `E_cap_month`
- No cross-reallocation between buckets

Additional economics:

- Treasury on-mint fee: `3%` of node gross (`B_node + S_node`)
- Staking commission: `7%` of node gross to LovePIPE pool (redistribution, not extra mint)

When both buckets are full:

```text
Minted_total = (B_node + S_node) + 0.03 * (B_node + S_node)
Upper bound: Minted_total <= 0.515 * E_cap_month
```

## 7) Base Rates and Quality Eligibility

USD-indexed rates (paid in PIPE at oracle price):

- CDN bandwidth: `$0.25` per TB delivered
- Storage capacity: `$0.25` per TB-month held

Payouts are flat-rate with no bonus tiers.

Minimum quality eligibility gates (pass/fail) for payout:

- Uptime: `>= 98%`
- Reliability error rate: `< 0.1%`
- Latency: within healthy band for route class
- Cache efficiency: `>= 80%` for CDN workload

Activation requirements:

- Minimum active stake per node in the LovePIPE pool: `STAKE_MIN = 100 PIPE`.
- Stake into LovePIPE pool: <https://www.jito.network/restaking/vaults/AoitBUHCmupYA61GrCdXWwU5KqFFVs2fLsAHayywFYRw/>
- `STAKE_MIN` can change with protocol updates.
- One payout wallet per node, and one node per payout wallet (strict 1:1 binding).
- LovePIPE unstake/withdraw timing is `jito_epoch`-based in Jito restaking, not a fixed 30-day lock.
- Current observed Jito epoch length on mainnet is `432000` slots (upstream parameter, can change).
- Under normal mainnet conditions, unlock timing is typically a few days, but can extend if state updates are delayed.

Stake-weighted work allocation (no rate change):

- For eligible nodes, higher stake can increase assignment priority for CDN egress jobs and storage placement jobs.
- Assignment priority uses a capped, diminishing-return function:
  - `a_i = min(PRIORITY_STAKE_CAP, sqrt(stake_i / STAKE_MIN))`
- `PRIORITY_STAKE_CAP` is a protocol parameter and can change with protocol updates.
- This affects assigned work volume, not payout rate.
- Payout rates remain fixed at `$0.25/TB` (CDN) and `$0.25/TB-month` (storage).

Ruthless enforcement rules:

- Any single gate breach during a settlement_epoch sets `q_i = 0` for that entire settlement_epoch.
- If active stake drops below `STAKE_MIN` at least once in a settlement_epoch, set `s_i = 0` for that settlement_epoch.
- If payout wallet is missing, changed, or shared with another node at least once in a settlement_epoch, set `w_i = 0` for that settlement_epoch.
- Settlement eligibility is `e_i = q_i * s_i * w_i`.
- `e_i` applies to both CDN and storage payouts for that settlement_epoch.
- No pro-rating, no grace windows, and no in-settlement_epoch manual override.
- Re-eligibility is evaluated at the next settlement_epoch boundary.

## 8) Per-Epoch Node Payout Formulas

Let:

- `P` = PIPE oracle price in USD
- `stake_i` = active stake for node `i`
- `q_i` = quality gate in `{0,1}`:
  - `q_i = 1` only if all quality gates pass for the full settlement_epoch
  - `q_i = 0` if any quality gate is breached at least once in the settlement_epoch
- `s_i` = stake gate in `{0,1}`:
  - `s_i = 1` only if active stake is `>= STAKE_MIN` for the full settlement_epoch
  - `s_i = 0` if active stake drops below `STAKE_MIN` at least once in the settlement_epoch
- `w_i` = wallet-binding gate in `{0,1}`:
  - `w_i = 1` only if exactly one payout wallet is bound to node `i`, and that wallet is not shared by any other node, for the full settlement_epoch
  - `w_i = 0` if wallet binding is missing, changed, or shared at least once in the settlement_epoch
- `e_i = q_i * s_i * w_i`
- `a_i = min(PRIORITY_STAKE_CAP, sqrt(stake_i / STAKE_MIN))`

Work allocation priority (within the same routing/placement queue):

```text
alloc_raw_i = a_i / sum_j(a_j)        # over eligible nodes in that queue
ramp_cap_i = NEW_NODE_QUEUE_SHARE_CAP if node_i is in ramp else 1
cluster_cap_i = remaining_cluster_cap_for(node_i)
alloc_bound_i = min(alloc_raw_i, MAX_QUEUE_SHARE, CLUSTER_QUEUE_SHARE_CAP, cluster_cap_i, ramp_cap_i)
alloc_share_i = redistribute_remaining_pro_rata(alloc_bound_i)
bw_assigned_i = bw_queue * alloc_share_i
st_assigned_i = st_queue * alloc_share_i
```

`redistribute_remaining_pro_rata` means leftover queue share from capped nodes is redistributed to other eligible, uncapped nodes in proportion to `a_i`.

Metered work used for payout is actual served/stored work:

- `bw_tb_i` = metered CDN TB delivered by node `i`
- `st_tbm_i` = metered storage TB-month by node `i`

Node raw USD work value:

```text
cdn_usd_i = bw_tb_i * 0.25 * e_i
st_usd_i  = st_tbm_i * 0.25 * e_i
```

Raw PIPE demand per node:

```text
cdn_raw_pipe_i = cdn_usd_i / P
st_raw_pipe_i  = st_usd_i / P
```

Bucket totals:

```text
B_raw = sum_i(cdn_raw_pipe_i)
S_raw = sum_i(st_raw_pipe_i)
```

Bucket caps and scale factors:

```text
B_cap   = 0.25 * E_cap_month
S_cap   = 0.25 * E_cap_month
B_scale = min(1, B_cap / B_raw)   # if B_raw > 0 else 0
S_scale = min(1, S_cap / S_raw)   # if S_raw > 0 else 0
```

Gross payout:

```text
gross_pipe_i = (cdn_raw_pipe_i * B_scale) + (st_raw_pipe_i * S_scale)
```

Net payout after staking commission:

```text
net_pipe_i = gross_pipe_i * 0.93
```

## 9) Executable Test Vectors

Narrative examples are intentionally removed from the policy body.

- Canonical deterministic vectors live in `docs/test-vectors/*.json`.
- CI executes these vectors with `docs/scripts/run_tokenomics_test_vectors.py`.
- Vectors cover nominal settlement, gate failures, oracle halt conditions, empty bucket demand, and cluster-cap binding.

## 10) Burn-to-Credit

Users may burn PIPE and receive USD-denominated usage credit at oracle price.

At burn time:

```text
credit_usd = PIPE_burned * PIPE_price_at_burn
```

Usage debits:

- CDN bandwidth: `$0.25/TB`
- Storage capacity: `$0.25/TB-month`

## 11) Node Operator Genesis Program

Purpose: bootstrap supply side and geo/ISP diversity.

- Budget: `100,000,000 PIPE` over 24 months
- Monthly cap: about `4,166,666 PIPE`
- Pools: `70/20/10` (Performance / Expansion / Special)
- Performance distribution basis: eligible useful work (no global boosts)

## 12) Oracle, Assignment, and Anti-Gaming Controls

- Oracle uses median/TWAP with deviation clamps and circuit breakers.
- Duplicate/replayed work is penalized.
- Minimum per-node active stake gate is enforced for eligibility (`STAKE_MIN`, default `100 PIPE`).
- Strict one-wallet-per-node payout binding is enforced for eligibility.
- Deterministic epoch snapshots:
  - Eligibility gates are evaluated across the full settlement_epoch event stream.
  - Assignment priority weight `a_i` is computed from stake at settlement_epoch start and is fixed for that settlement_epoch.
  - Any in-settlement_epoch payout wallet change or wallet-sharing event sets `w_i = 0` for that settlement_epoch.
- Fail-closed telemetry and oracle rules:
  - Required quality telemetry must be present for the full settlement_epoch.
  - If required telemetry is missing for more than `TELEMETRY_MAX_GAP_SECONDS`, set `q_i = 0`.
  - Telemetry arriving later than `TELEMETRY_MAX_DELAY_SECONDS` is excluded from that settlement_epoch settlement.
  - If settlement oracle price age exceeds `ORACLE_MAX_AGE_SECONDS`, global settlement is halted (no payouts are executed) until a valid oracle value is available.
- Assignment concentration and anti-sybil controls:
  - Per-node queue share cap: `MAX_QUEUE_SHARE = 20%`.
  - Related-node cluster queue cap: `CLUSTER_QUEUE_SHARE_CAP = 25%`.
  - New-node ramp: first `NEW_NODE_RAMP_EPOCHS = 2` settlement_epochs capped at `NEW_NODE_QUEUE_SHARE_CAP = 5%` per queue.
  - Excess assignment above caps is redistributed pro-rata to remaining eligible nodes in the same queue.
  - Identity clustering can use payout wallet, stake authority, node identity, IP/ASN correlation, and host fingerprint signals.
  - If sybil risk cannot be resolved, node enters assignment hold (`ASSIGNMENT_HOLD = 1`) until cleared.
- Suspension and reactivation state machine:
  - States: `ACTIVE`, `SUSPENDED`, `REENTRY_RAMP`.
  - If `e_i = 0`, increment failure streak for that node.
  - If failure streak reaches `FAIL_STREAK_SUSPEND_THRESHOLD = 3`, transition to `SUSPENDED` for `SUSPEND_EPOCHS = 1` settlement_epoch.
  - After suspension, transition to `REENTRY_RAMP` for `NEW_NODE_RAMP_EPOCHS` settlement_epochs.
  - After successful ramp settlement_epochs, return to `ACTIVE`. Any failed settlement_epoch in ramp restarts suspension logic.
- Per-settlement_epoch accounting commitments should remain externally auditable.

### Incident Runbooks

#### Oracle Halt

- Trigger: settlement oracle age `> ORACLE_MAX_AGE_SECONDS`.
- Immediate action: set global settlement state to `HALT`; do not execute payouts.
- Recovery action: restore valid oracle feed, verify age is within bounds, and re-run deterministic settlement for affected settlement_epoch(s).
- Post-incident: publish halt interval, affected settlement_epoch(s), and replay outcome in monthly report.

#### Telemetry Gap Incident

- Trigger: required telemetry gap `> TELEMETRY_MAX_GAP_SECONDS` for a node.
- Immediate action: set `q_i = 0` for impacted settlement_epoch by fail-closed rule.
- Recovery action: restore telemetry pipeline; verify freshness and delay bounds before next settlement_epoch.
- Post-incident: publish affected nodes and telemetry exclusion counts.

#### Assignment Hold Incident

- Trigger: unresolved sybil-risk signal or identity-cluster conflict.
- Immediate action: set `ASSIGNMENT_HOLD = 1` for impacted node/cluster; stop new assignment.
- Recovery action: clear conflicting identity signals and verify cluster-cap compliance.
- Post-incident: publish hold start/end, reason code, and release criteria met.

## 13) Public Monthly Reporting

Publish at least:

- `policy_version`
- `policy_checksum_sha256` (computed from `docs/Tokenomics.md` + `docs/tokenomics-params.json`)
- `S_year_start`, `r_y`, `E_cap_month`
- `effective_settlement_epoch`
- `node_bw_minted`, `node_st_minted`
- `staking_commission_to_pool`
- `treasury_on_mint`
- `mint_total`
- per-node active stake status and threshold breaches
- per-node payout wallet binding status and conflict events
- per-node telemetry gap events and late-telemetry exclusions
- oracle freshness status and any settlement halt events
- per-node suspension state and failure streak count
- sybil-risk cluster flags and assignment-hold events
- burn totals and `net_supply_change`

### Settlement Output Schema (Reference)

Each monthly settlement report should emit machine-verifiable records with these fields:

| Field | Type | Unit | Description |
| --- | --- | --- | --- |
| `policy_version` | string | n/a | Tokenomics policy version used for settlement. |
| `policy_checksum_sha256` | string | hex | SHA-256 over canonical policy artifacts. |
| `effective_settlement_epoch` | string | `YYYY-MM` | Settlement window identifier. |
| `node_id` | string | pubkey | Node identity key. |
| `payout_wallet` | string | pubkey | Bound payout wallet for node. |
| `q_i` | integer | boolean (`0/1`) | Quality gate result. |
| `s_i` | integer | boolean (`0/1`) | Stake gate result. |
| `w_i` | integer | boolean (`0/1`) | Wallet-binding gate result. |
| `e_i` | integer | boolean (`0/1`) | Combined eligibility gate. |
| `bw_tb_i` | number | TB | Metered CDN egress. |
| `st_tbm_i` | number | TB-month | Metered storage capacity. |
| `cdn_usd_i` | number | USD | Raw CDN value before bucket scaling. |
| `st_usd_i` | number | USD | Raw storage value before bucket scaling. |
| `cdn_raw_pipe_i` | number | PIPE | Raw CDN PIPE demand. |
| `st_raw_pipe_i` | number | PIPE | Raw storage PIPE demand. |
| `B_scale` | number | ratio | CDN bucket scaling factor. |
| `S_scale` | number | ratio | Storage bucket scaling factor. |
| `gross_pipe_i` | number | PIPE | Gross payout before staking commission. |
| `net_pipe_i` | number | PIPE | Net payout after commission and rounding. |
| `settlement_state` | string | enum | `OK` or `HALT`. |

## 14) Parameter Registry (Defaults)

All protocol-updateable rows must be activated only at a settlement boundary via:

- `effective_settlement_epoch`

| Parameter | Current Value | Unit | Min | Max | Enforced Where | Protocol-Updateable | Change Effective Field | Parameter Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CDN_RATE_USD_PER_TB` | `0.25` | USD/TB | `0.01` | `5.00` | Off-chain settlement engine | Yes | `effective_settlement_epoch` | Economics |
| `STORAGE_RATE_USD_PER_TB_MONTH` | `0.25` | USD/TB-month | `0.01` | `5.00` | Off-chain settlement engine | Yes | `effective_settlement_epoch` | Economics |
| `BW_BUCKET_CAP_PCT` | `25` | % of monthly cap | `0` | `50` | Off-chain settlement engine | Yes | `effective_settlement_epoch` | Economics |
| `ST_BUCKET_CAP_PCT` | `25` | % of monthly cap | `0` | `50` | Off-chain settlement engine | Yes | `effective_settlement_epoch` | Economics |
| `TREASURY_ON_MINT_FEE_BPS` | `300` | bps | `0` | `1000` | Off-chain settlement engine | Yes | `effective_settlement_epoch` | Economics |
| `STAKING_COMMISSION_BPS` | `700` | bps | `0` | `2000` | Off-chain settlement engine | Yes | `effective_settlement_epoch` | Economics |
| `PIPE_DECIMALS` | `6` | decimal places | `n/a` | `n/a` | Off-chain settlement output | No | `n/a` | Settlement Engineering |
| `SETTLEMENT_ROUNDING_MODE` | `round_down` | enum | `n/a` | `n/a` | Off-chain settlement output | No | `n/a` | Settlement Engineering |
| `STAKE_MIN` | `100` | PIPE per node | `100` | `100000` | Off-chain eligibility checker | Yes | `effective_settlement_epoch` | Economics |
| `PRIORITY_STAKE_CAP` | `4.0` | weight ratio cap | `1.0` | `8.0` | Off-chain assignment scheduler | Yes | `effective_settlement_epoch` | Assignment Engineering |
| `MAX_QUEUE_SHARE` | `20` | % per node per queue per settlement_epoch | `5` | `50` | Off-chain assignment scheduler | Yes | `effective_settlement_epoch` | Assignment Engineering |
| `CLUSTER_QUEUE_SHARE_CAP` | `25` | % per related-node cluster per queue per settlement_epoch | `10` | `60` | Off-chain assignment scheduler | Yes | `effective_settlement_epoch` | Assignment Engineering |
| `NEW_NODE_RAMP_EPOCHS` | `2` | settlement_epochs | `0` | `6` | Off-chain assignment scheduler | Yes | `effective_settlement_epoch` | Assignment Engineering |
| `NEW_NODE_QUEUE_SHARE_CAP` | `5` | % per queue in ramp | `1` | `10` | Off-chain assignment scheduler | Yes | `effective_settlement_epoch` | Assignment Engineering |
| `FAIL_STREAK_SUSPEND_THRESHOLD` | `3` | failed settlement_epochs | `1` | `6` | Off-chain assignment scheduler | Yes | `effective_settlement_epoch` | Reliability Engineering |
| `SUSPEND_EPOCHS` | `1` | settlement_epochs | `1` | `6` | Off-chain assignment scheduler | Yes | `effective_settlement_epoch` | Reliability Engineering |
| `TELEMETRY_MAX_GAP_SECONDS` | `900` | seconds | `60` | `3600` | Off-chain eligibility checker | Yes | `effective_settlement_epoch` | Observability Engineering |
| `TELEMETRY_MAX_DELAY_SECONDS` | `3600` | seconds | `300` | `86400` | Off-chain eligibility checker | Yes | `effective_settlement_epoch` | Observability Engineering |
| `ORACLE_MAX_AGE_SECONDS` | `3600` | seconds | `60` | `21600` | Off-chain settlement engine | Yes | `effective_settlement_epoch` | Oracle Operations |
| `PAYOUT_WALLET_BINDING_MODE` | `1:1 strict` | enum | `n/a` | `n/a` | Off-chain eligibility checker | No | `n/a` | Protocol Ops |
| `JITO_EPOCH_LENGTH_SLOTS` | `432000` | slots | `n/a` | `n/a` | On-chain Jito config | No (external upstream) | `n/a` | Jito (External) |
| `LOVEPIPE_UNSTAKE_TIMING_MODE` | `epoch_based` | enum | `n/a` | `n/a` | On-chain Jito + off-chain settlement ops | No (external upstream) | `n/a` | Jito + Protocol Ops |
| `GLOBAL_BOOST_PROGRAMS` | `disabled` | boolean | `n/a` | `n/a` | Policy + off-chain settlement engine | No | `n/a` | Economics |

## 15) Symbols

- `r_y`: annual nominal inflation cap for year `y`
- `E_cap_month`: monthly mint cap
- `S_year_start`: circulating supply at start of year
- `settlement_epoch`: monthly accounting and payout window
- `jito_epoch`: slot-based Jito restaking epoch
- `effective_settlement_epoch`: settlement window when a parameter change becomes active
- `B_raw`, `S_raw`: raw network payout demand per bucket
- `B_cap`, `S_cap`: bucket caps
- `q_i`: quality gate (`0` or `1`)
- `s_i`: stake gate (`0` or `1`)
- `w_i`: payout wallet-binding gate (`0` or `1`)
- `e_i`: combined epoch eligibility gate (`q_i * s_i * w_i`)
- `stake_i`: active stake for node `i`
- `a_i`: stake-based allocation priority weight
- `alloc_share_i`: queue assignment share for node `i`
- `cluster_cap_i`: remaining assignment cap for the related-node cluster of node `i`
- `STAKE_MIN`: minimum required active stake per node
- `PRIORITY_STAKE_CAP`: cap on stake-priority weight
- `MAX_QUEUE_SHARE`: per-node queue assignment share cap
- `CLUSTER_QUEUE_SHARE_CAP`: per-cluster queue assignment share cap
- `NEW_NODE_RAMP_EPOCHS`: number of initial settlement_epochs using ramp caps
- `NEW_NODE_QUEUE_SHARE_CAP`: per-node queue cap during ramp
- `FAIL_STREAK_SUSPEND_THRESHOLD`: failed-settlement_epoch streak that triggers assignment suspension
- `SUSPEND_EPOCHS`: duration of assignment suspension in settlement_epochs
- `TELEMETRY_MAX_GAP_SECONDS`: max allowed telemetry gap before fail-closed ineligibility
- `TELEMETRY_MAX_DELAY_SECONDS`: max allowed telemetry delay before exclusion from settlement_epoch
- `ORACLE_MAX_AGE_SECONDS`: max oracle staleness before settlement halt
- `PIPE_DECIMALS`: payout output decimal precision
- `P`: PIPE USD oracle price

## 16) Disclaimer

This document is informational policy guidance and not legal, tax, or investment advice.
