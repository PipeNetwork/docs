# Tokenomics Internal Operations Notes

Metadata: Internal operations reference, aligned to public policy `v2.6.0`.

This document contains internal runbooks and reporting guidance intentionally excluded from public tokenomics docs.

## 1) Incident Runbooks

### Oracle Halt

- Trigger: settlement oracle age `> ORACLE_MAX_AGE_SECONDS`.
- Immediate action: set global settlement state to `HALT`; do not execute payouts.
- Recovery action: restore valid oracle feed, verify age is within bounds, and re-run deterministic settlement for affected settlement_epoch(s).
- Post-incident: publish halt interval, affected settlement_epoch(s), and replay outcome in monthly report.

### Telemetry Gap Incident

- Trigger: required telemetry gap `> TELEMETRY_MAX_GAP_SECONDS` for a node.
- Immediate action: set `q_i = 0` for impacted settlement_epoch by fail-closed rule.
- Recovery action: restore telemetry pipeline; verify freshness and delay bounds before next settlement_epoch.
- Post-incident: publish affected nodes and telemetry exclusion counts.

### Assignment Hold Incident

- Trigger: unresolved sybil-risk signal or identity-cluster conflict.
- Immediate action: set `ASSIGNMENT_HOLD = 1` for impacted node/cluster; stop new assignment.
- Recovery action: clear conflicting identity signals and verify cluster-cap compliance.
- Post-incident: publish hold start/end, reason code, and release criteria met.

## 2) Public Monthly Reporting (Internal Checklist)

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
- `net_supply_change`

### Settlement Output Schema (Reference)

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

## 3) Symbols

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
