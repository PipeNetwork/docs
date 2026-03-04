# Tokenomics Operations Spec (Mainnet)

Metadata: `Version 2.6.0` | Effective Date: March 3, 2026 | Status: Active

This public operations spec contains deterministic settlement math and the parameter registry used by Mainnet tokenomics.

## 1) Deterministic Settlement Math

Deterministic settlement rules:

- Internal work accounting is byte-level and timestamped.
- Settlement arithmetic uses fixed-point decimal with at least 18 decimal places internally.
- Processing order is fixed:
  1. Compute `bw_tb_i` and `st_tbm_i` from metered bytes/time.
  2. Apply eligibility gate `e_i`.
  3. Compute USD values at fixed rates (`$0.25/TB`, `$0.25/TB-month`).
  4. Convert USD to raw PIPE using settlement_epoch oracle price `P`.
  5. Apply bucket scaling (`B_scale`, `S_scale`).
  6. Apply staking commission (`7%`) to get `net_pipe_i`.
  7. Round `net_pipe_i` down to `PIPE_DECIMALS = 6`.
- Final payout rounding mode is `round_down`.
- Tie-break rules where equal ordering is possible:
  - Node ordering uses ascending node identity public key bytes.
  - If equal stake priority weights in scheduling, assign using the same node-key sort order.

Settlement variables:

- `P` = PIPE oracle price in USD
- `stake_i` = active stake for node `i`
- `q_i`, `s_i`, `w_i` in `{0,1}`
- `e_i = q_i * s_i * w_i`
- `a_i = min(PRIORITY_STAKE_CAP, sqrt(stake_i / STAKE_MIN))`
- Assignment share values in this section are fractions in `[0,1]`.
- Percentage cap parameters (`MAX_QUEUE_SHARE`, `CLUSTER_QUEUE_SHARE_CAP`, `NEW_NODE_QUEUE_SHARE_CAP`) are normalized with `/100` before comparisons.

Work allocation priority (within the same routing/placement queue):

```text
alloc_raw_i = a_i / sum_j(a_j)                                # over eligible nodes in that queue
max_queue_share = MAX_QUEUE_SHARE / 100
cluster_queue_share_cap = CLUSTER_QUEUE_SHARE_CAP / 100
ramp_cap_i = (NEW_NODE_QUEUE_SHARE_CAP / 100) if node_i is in ramp else 1
cluster_cap_i = remaining_cluster_cap_for(node_i)             # fraction in [0,1]
alloc_bound_i = min(alloc_raw_i, max_queue_share, cluster_queue_share_cap, cluster_cap_i, ramp_cap_i)
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

Gross and net payout:

```text
gross_pipe_i = (cdn_raw_pipe_i * B_scale) + (st_raw_pipe_i * S_scale)
net_pipe_i = gross_pipe_i * 0.93
```

## 2) Parameter Registry (Defaults)

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
