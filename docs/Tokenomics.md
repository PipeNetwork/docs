# Pipe Network Mainnet Tokenomics Policy

Metadata: `Version 2.6.0` | Effective Date: March 3, 2026 | Status: Active

This document is the canonical reference for Mainnet payout rules.

## Non-Negotiables

- CDN payout rate is fixed at `$0.25/TB`.
- Storage capacity payout rate is fixed at `$0.25/TB-month`.
- Minimum active stake per node is `100 PIPE` in LovePIPE.
- Payout wallet binding is strict `1:1` (one node per wallet, one wallet per node).
- Any gate breach in a settlement_epoch makes the node ineligible for that full settlement_epoch.
- Pricing scope is fixed to CDN bandwidth and storage capacity; storage bandwidth pricing is out of scope.

## 1) Scope

- Network: Mainnet
- Chain: Solana (SPL token)
- Token: PIPE
- Model: Proof-of-Useful-Work (PoUW) for CDN bandwidth and storage capacity

This policy does not define storage bandwidth pricing.

### Epoch Terminology

- `settlement_epoch`: the monthly accounting and payout window used by this policy.
- `jito_epoch`: the slot-based epoch used by Jito restaking (currently observed at `432000` slots on mainnet; upstream-configurable).
- Unless explicitly stated otherwise, "epoch" means `settlement_epoch`.

## 2) Units and Metering

- `1 TB = 1,000,000,000,000 bytes` (decimal, not TiB)
- `1 TB-month = 1 TB held for a full calendar month settlement_epoch`
- CDN bandwidth work counts successful edge egress bytes delivered to clients.
- Storage capacity work counts average stored bytes over the settlement_epoch.

Storage capacity proration:

```text
storage_tb_month_i = (sum_over_settlement_epoch_days(avg_stored_bytes_i_day) / 1e12) / days_in_settlement_epoch
```

Settlement output rounding is `round_down` to `PIPE_DECIMALS = 6` at final payout output.
Detailed settlement ordering and tie-break rules are defined in [Tokenomics Operations Spec](tokenomics-operations-spec.md).

## 3) Mainnet Base Rates

- CDN bandwidth: `$0.25` per TB delivered
- Storage capacity: `$0.25` per TB-month held
- Payout rates are flat. No bonus tiers.

## 4) Activation and Hard-Fail Eligibility

- Stake requirement: minimum active stake per node in LovePIPE is `STAKE_MIN = 100 PIPE`.
- Stake link: <https://www.jito.network/restaking/vaults/AoitBUHCmupYA61GrCdXWwU5KqFFVs2fLsAHayywFYRw/>
- `STAKE_MIN` can change with protocol updates.
- Wallet binding requirement: one payout wallet per node, and one node per payout wallet (strict `1:1`).

Eligibility gates are fail-closed:

| Rule | Threshold / Requirement | Breach Result |
| --- | --- | --- |
| Uptime | `>= 98%` for full settlement_epoch | `q_i = 0` for that settlement_epoch |
| Reliability error rate | `< 0.1%` for full settlement_epoch | `q_i = 0` for that settlement_epoch |
| Latency | Within healthy band for route class for full settlement_epoch | `q_i = 0` for that settlement_epoch |
| CDN cache efficiency | `>= 80%` for CDN workload for full settlement_epoch | `q_i = 0` for that settlement_epoch |
| Active stake | `stake_i >= STAKE_MIN` for full settlement_epoch | `s_i = 0` for that settlement_epoch |
| Wallet binding | Exactly one payout wallet per node and no shared payout wallet for full settlement_epoch | `w_i = 0` for that settlement_epoch |

Stake gate adjudication (`s_i`) is deterministic:

- Data source: finalized on-chain LovePIPE stake records for each node.
- Sampling cadence: hourly snapshots across the full settlement_epoch.
- Pass condition: every snapshot must satisfy `stake_i >= STAKE_MIN`.
- Any snapshot below `STAKE_MIN` sets `s_i = 0` for the full settlement_epoch.
- `STAKE_MIN` updates activate only at `effective_settlement_epoch` boundaries.

Combined settlement eligibility:

```text
e_i = q_i * s_i * w_i
```

Ruthless enforcement:

- Any single breach sets ineligibility for the full settlement_epoch.
- No pro-rating, no grace windows, and no in-settlement_epoch manual override.
- Re-eligibility is evaluated at the next settlement_epoch boundary.

Assignment note:

- Higher stake can increase assignment priority for CDN egress and storage placement jobs.
- Assignment priority changes work volume only; it never changes payout rates.

LovePIPE unstake timing:

- Unstake and withdraw timing is `jito_epoch`-based, not a fixed 30-day lock.
- Current observed Jito epoch length on mainnet is `432000` slots (upstream parameter, can change).

## 5) Canonical Payout Formula

Definitions:

- `P`: PIPE oracle price in USD for settlement_epoch
- `bw_tb_i`: metered CDN TB delivered by node `i`
- `st_tbm_i`: metered storage TB-month by node `i`
- `e_i`: combined eligibility gate (`0` or `1`)
- `B_scale`, `S_scale`: bucket scaling factors from [Tokenomics Operations Spec](tokenomics-operations-spec.md)

Canonical settlement formulas:

```text
cdn_usd_i      = bw_tb_i * 0.25 * e_i
st_usd_i       = st_tbm_i * 0.25 * e_i
cdn_raw_pipe_i = cdn_usd_i / P
st_raw_pipe_i  = st_usd_i / P
gross_pipe_i   = (cdn_raw_pipe_i * B_scale) + (st_raw_pipe_i * S_scale)
net_pipe_i     = floor_6(gross_pipe_i * 0.93)
```

## Implementation References

- Settlement math and parameter registry: [Tokenomics Operations Spec](tokenomics-operations-spec.md)
- Machine-readable parameter registry: [tokenomics-params.json](tokenomics-params.json)
- Deterministic vectors: `docs/test-vectors/*.json`

## Disclaimer

This document is informational policy guidance and not legal, tax, or investment advice.
