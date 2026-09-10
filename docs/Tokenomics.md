# Pipe Network Tokenomics

Metadata: `Version 3.0.0` | Updated: September 10, 2026 | Status: Current documentation

Pipe Network's storage model supports the long-term operation of the protocol through useful storage capacity and revenue-funded token buybacks. **Running a node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.**

## Node Participation

Each node wallet must hold LovePIPE liquid staking tokens (LSTs), also called vault receipt tokens (VRTs), representing at least **10,000 PIPE**. The requirement is measured in underlying PIPE, not a fixed number of LovePIPE tokens. Operators can deposit PIPE into LovePIPE or transfer an existing LovePIPE position into the node wallet.

The control plane verifies current ownership using finalized Solana state every UTC hour. Under ordinary public admission, a node must pass every hourly check in one complete UTC calendar month before becoming eligible for routing, and maintain the required position while active. Each node uses its own wallet; the same position cannot qualify multiple nodes.

Missing, invalid, or below-threshold observations invalidate the qualification month. An active node that fails ownership or balance verification is removed from routing and must complete a new valid month to qualify again. Health, capacity, enrollment, and storage integrity checks also apply.

Stake affects eligibility and placement priority. It does not create an entitlement to payment for running a node. See the [node setup guide](nodes/mainnet.md), [wallet guide](nodes/wallet-setup.md), and [eligibility checklist](nodes/mainnet-quality-standards.md).

## No Individual Node Rewards

Storage, bandwidth, uptime, receipts, and repair work do not accrue rewards or payouts to individual nodes. There are no per-TB operator payments, node reward emissions, or location bonuses under this model. Customer storage charges fund the protocol's service; they do not become a payable balance for the node that serves a request. Net revenue is determined separately under the protocol's accounting policy.

Running a storage node contributes capacity, availability, and resilience to the protocol over the long term. Operators contribute the resources and operating costs needed to provide that service. Removing individual node rewards avoids recurring node-payment obligations and reward-driven token emissions, supporting the protocol's long-term sustainability.

## Net Revenue, Buyback and Burn, and LovePIPE

A percentage of net protocol revenue will be used to buy back and burn PIPE. A LovePIPE pool contribution equal to **7% of the monthly revenue amount designated for the buyback program** will increase the backing of existing LSTs for everyone staking.

The following accounting details remain to be specified:

- The percentage of net revenue committed to the program and its effective month.
- The accounting definition of net revenue, including deductions and execution costs.
- Whether the LovePIPE contribution is taken from the buyback allocation or funded in addition to it.
- The execution and vault-accounting mechanism used to increase backing for existing LST holders.

For a monthly buyback reference amount of $10,000, the LovePIPE contribution is $700. This example does not determine the remaining burn budget or total treasury spending, because the contribution's funding treatment has not been finalized. Actual PIPE quantities depend on completed purchases.

The 7% is a share of the monthly buyback reference amount, not of all protocol revenue and not a commission on node earnings. PIPE contributed to LovePIPE remains pool backing and is not also counted as burned.

## How LovePIPE Stakers Benefit

LovePIPE represents a proportional claim on PIPE held in the pool. Adding PIPE to the backing of existing LSTs increases the PIPE represented by each LST. This benefits all LovePIPE stakers, including those who do not run nodes. A node operator participates in this benefit through their LovePIPE holdings on the same basis as other stakers, without receiving a separate node reward.

The 7% contribution is a revenue allocation, not a 7% staking yield. The benefit depends on the monthly allocation, the PIPE acquired, and the pool's backing and outstanding LST supply. It describes growth in underlying PIPE backing per token, not a guaranteed market price.

Deposits and withdrawals use the existing LovePIPE vault. Withdrawal timing follows the vault's current on-chain configuration and is separate from the node's calendar-month qualification period.

## Implementation and References

The storage implementation already verifies LovePIPE eligibility and records customer credit usage without creating node earnings. The monthly revenue allocation, buybacks, burns, and LovePIPE contributions described here are treasury policy; this documentation does not establish that automated treasury execution is deployed.

- [Tokenomics Operations Spec](tokenomics-operations-spec.md): allocation accounting and implementation boundaries.
- [Parameter registry](tokenomics-params.json): machine-readable policy values, including the unspecified net-revenue percentage.
- [Storage overview](storage/overview.md): customer access and storage-node responsibilities.
- [LovePIPE](https://pipe.love): staking interface for the existing vault.
