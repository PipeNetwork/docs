# Tokenomics Operations Spec

Metadata: `Version 3.1.1` | Updated: September 27, 2026 | Status: Current documentation

This document accompanies the [tokenomics policy](Tokenomics.md). It separates implemented node eligibility and customer accounting from optional treasury actions.

## 1) Treasury Actions

Treasury may use protocol revenue to support PIPE, for example through buybacks, burns, or LovePIPE backing. Those actions are optional and are reported when they are executed. There is no published percentage of net revenue and no executable monthly allocation formula.

```text
individual_node_rewards = 0
```

The storage service does not implement a treasury workflow. Customer credit usage is not a node payout and is not by itself a published treasury allocation.

If treasury executes such an action, report what was actually purchased, burned, or contributed, with transaction references and costs. Do not present a planned allocation as a completed transaction. An ordinary LovePIPE deposit that issues a proportional new LST position to the depositor does not by itself increase backing per existing LST.

## 2) Parameter Registry (Defaults)

This registry describes the current protocol documentation. It lists implemented eligibility and accounting policy. It does not invent treasury percentages or incomplete buyback parameters.

| Parameter | Current Value | Unit | Min | Max | Enforced Where | Protocol-Updateable | Change Effective Field | Parameter Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `STAKE_MIN` | `10000` | underlying PIPE per node | `n/a` | `n/a` | Control-plane LovePIPE eligibility | Explicit protocol release | qualification month | Protocol |
| `NODE_REWARDS_ENABLED` | `false` | boolean | `n/a` | `n/a` | Storage service; node payments removed | Explicit protocol release | release | Protocol |
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

The control plane verifies ownership, vault and mint identity, and the conversion inputs. Ordinary public admission is invite-only. It also requires the 10,000 PIPE LovePIPE minimum and a complete UTC calendar month of passing hourly checks. There is no public waitlist and no self-serve enrollment form. Operators who want to run a node may email [hello@pipe.network](mailto:hello@pipe.network) to inquire. Installing node software does not enroll a node. Placement additionally depends on node health, available capacity, and the storage policy; priority is not a guaranteed assignment share or financial return.

Missing or invalid observations fail qualification. Ownership or balance failures remove an active node from routing. Administrators can blacklist nodes, but the storage control plane does not seize, burn, withdraw, or transfer LovePIPE positions.

Private bootstrap exemptions may exist. They are administered by the protocol, are not a public enrollment path, create no rewards, and do not change the public 10,000 PIPE requirement. Detailed exemption mechanics are not published here.

This documentation revision is `3.1.1`. It does not change the Lattice implementation eligibility policy identifier `v2.6.0`. The reviewed implementation still enforces the 10,000 PIPE minimum. Updating these documents is not a protocol release and does not deploy a new configuration.

## 4) Reporting

Keep customer USDC receipts and credit usage separate from revenue recognition and any treasury execution. Prepaid customer credit is not automatically the same as recognized net revenue. Node service metrics are operational evidence and must not be presented as unpaid reward balances.

If treasury supports PIPE in a given period, record the actual PIPE purchased, burned, or contributed, transaction references, execution costs, and remaining balances. Do not publish a net-revenue allocation percentage that has not been committed.
