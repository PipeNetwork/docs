# Tokenomics Operations Spec

Metadata: `Version 3.0.0` | Updated: September 10, 2026 | Status: Current documentation

This document accompanies the [tokenomics policy](Tokenomics.md). It separates implemented node eligibility and customer accounting from the monthly revenue allocation policy.

## 1) Monthly Revenue Allocation

Define `N_month` as net protocol revenue on the published accounting basis and `r` as the fraction committed to the buyback program. The percentage `r` remains unspecified.

```text
monthly_buyback_reference_amount = N_month * r
lovepipe_contribution_budget = monthly_buyback_reference_amount * 0.07
individual_node_rewards = 0
```

These formulas apply once the revenue basis and percentage have been published. They do not set the actual burn budget or total treasury outflow: the funding treatment of the LovePIPE contribution remains unspecified. Do not assume it is deducted from the reference amount, or added on top, until that treatment is defined. Do not convert an unspecified percentage into zero.

For a $10,000 monthly buyback reference amount, the LovePIPE contribution budget is $700. Currency budgets are separate from actual PIPE quantities, execution costs, unspent amounts, and completed burns. No positive revenue-funded amount follows from zero or negative net revenue; any use of reserves requires its own documented accounting treatment.

The contribution mechanism must increase the PIPE backing of existing LSTs. An ordinary deposit that issues a proportional new LST position to the depositor does not by itself increase backing per existing LST. Treasury execution must account for the actual vault state, outstanding supply, fees, and contribution recognition.

Publish the net-revenue basis, percentage and effective month, contribution funding treatment, execution costs, rounding and remainder handling, and vault contribution mechanism before reporting an executable monthly allocation. The storage service does not implement this treasury workflow.

## 2) Parameter Registry (Defaults)

This registry describes the current documentation policy. Rows marked as treasury policy are not claims of runtime enforcement. `unspecified` is an explicit missing policy value, not a numeric setting.

| Parameter | Current Value | Unit | Min | Max | Enforced Where | Protocol-Updateable | Change Effective Field | Parameter Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `STAKE_MIN` | `10000` | underlying PIPE per node | `n/a` | `n/a` | Control-plane LovePIPE eligibility | Explicit protocol release | qualification month | Protocol |
| `NODE_REWARDS_ENABLED` | `false` | boolean | `n/a` | `n/a` | Storage service; node payments removed | Explicit protocol release | release | Protocol |
| `NET_REVENUE_ALLOCATION_PCT` | `unspecified` | % of monthly net revenue | `0` | `100` | Treasury policy; execution not established | Yes | reporting month | Treasury |
| `LOVEPIPE_ALLOCATION_BPS` | `700` | basis points of monthly buyback reference amount | `n/a` | `n/a` | Treasury policy; execution not established | Explicit policy update | reporting month | Treasury |
| `LOVEPIPE_FUNDING_TREATMENT` | `unspecified` | allocation deduction or additional funding | `n/a` | `n/a` | Treasury policy; execution not established | Explicit policy update | reporting month | Treasury |
| `PRIORITY_STAKE_CAP` | `4.0` | placement priority cap | `n/a` | `n/a` | Control-plane signed topology | Explicit protocol release | qualification month | Protocol |
| `STAKE_SNAPSHOT_INTERVAL_SECONDS` | `3600` | seconds; aligned to UTC hours | `n/a` | `n/a` | Control-plane LovePIPE verifier | Explicit protocol release | qualification month | Protocol |
| `QUALIFICATION_PERIOD` | `one_complete_utc_calendar_month` | calendar period | `n/a` | `n/a` | Control-plane LovePIPE eligibility | Explicit protocol release | qualification month | Protocol |
| `NODE_WALLET_BINDING` | `1:1` | node identity to Solana wallet | `n/a` | `n/a` | Control-plane enrollment and ownership checks | Explicit protocol release | release | Protocol |

## 3) Implemented Storage Accounting and Eligibility

The current serving profile uses control-plane coordination and internal customer credits. Customers purchase storage credit with USDC on Solana. Authorized storage operations reserve and debit that credit; signed node receipts and matching router reports provide integrity and accounting evidence. Receipt acceptance does not create node earnings. The service has no earnings or payout-export endpoint and rejects the retired on-chain node-payment backend.

LovePIPE eligibility uses finalized vault and wallet state:

```text
pipe_equivalent_atoms = floor(vrt_atoms * vault_pipe_atoms / vrt_supply_atoms)
priority = min(4.0, sqrt(pipe_equivalent / 10000))
```

The control plane verifies ownership, vault and mint identity, and the conversion inputs. Under ordinary public admission, every hourly snapshot in a complete UTC calendar month must pass. Placement additionally depends on node health, available capacity, and the storage policy; priority is not a guaranteed assignment share or financial return.

Missing or invalid observations fail qualification. Ownership or balance failures remove an active node from routing. Administrators can blacklist nodes, but the storage control plane does not seize, burn, withdraw, or transfer LovePIPE positions.

The protocol can grant narrowly scoped bootstrap exemptions to enrolled identities through its private operator controls. Exemptions create no rewards and do not bypass node health, integrity, or blacklist checks. They do not change the public 10,000 PIPE participation requirement.

This documentation revision is `3.0.0`. The reviewed Lattice implementation still identifies its eligibility policy as `v2.6.0` and enforces the 10,000 PIPE minimum. Updating these documents does not change that runtime identifier or deploy a new configuration.

## 4) Monthly Reporting

Report the net-revenue basis, allocation percentage, LovePIPE funding treatment, monthly buyback reference amount, actual budget for each destination, actual PIPE purchased, PIPE burned, PIPE contributed to LovePIPE, transaction references, execution costs, and unspent balances. Record the contribution's effect on underlying PIPE per LST using the vault's actual accounting state.

Keep customer USDC receipts and credit usage separate from revenue recognition and treasury execution. Prepaid customer credit is not automatically the same as recognized net revenue. Node service metrics are operational evidence and must not be presented as unpaid reward balances.
