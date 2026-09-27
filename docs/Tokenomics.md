# Pipe Network Tokenomics

Metadata: `Version 3.1.0` | Updated: September 27, 2026 | Status: Current documentation

Pipe Network's storage model supports the long-term operation of the protocol through useful storage capacity. **Running a Lattice Firestarter node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.**

## Node Participation

Each node wallet must hold LovePIPE liquid staking tokens (LSTs), also called vault receipt tokens (VRTs), representing at least **10,000 PIPE**. The requirement is measured in underlying PIPE, not a fixed number of LovePIPE tokens. Operators can deposit PIPE into LovePIPE or transfer an existing LovePIPE position into the node wallet.

The control plane verifies current ownership using finalized Solana state every UTC hour. Under ordinary public admission, a node must pass every hourly check in one complete UTC calendar month before becoming eligible for routing, and maintain the required position while active. Each node uses its own wallet; the same position cannot qualify multiple nodes.

Missing, invalid, or below-threshold observations invalidate the qualification month. An active node that fails ownership or balance verification is removed from routing and must complete a new valid month to qualify again. Health, capacity, enrollment, and storage integrity checks also apply.

Stake affects eligibility and placement priority. It does not create an entitlement to payment for running a node. See the [node setup guide](nodes/mainnet.md), [wallet guide](nodes/wallet-setup.md), and [eligibility checklist](nodes/mainnet-quality-standards.md).

## No Individual Node Rewards

Storage, bandwidth, uptime, receipts, and repair work do not accrue rewards or payouts to individual nodes. There are no per-TB operator payments, node reward emissions, or location bonuses under this model. Customer storage charges fund the protocol's service; they do not become a payable balance for the node that serves a request.

Running a Lattice Firestarter node contributes capacity, availability, and resilience to the protocol over the long term. Operators contribute the resources and operating costs needed to provide that service. Removing individual node rewards avoids recurring node-payment obligations and reward-driven token emissions, supporting the protocol's long-term sustainability.

## Treasury Policy

Treasury may use protocol revenue to support PIPE—for example through buybacks, burns, or contributions that increase LovePIPE backing. Those actions are optional. Treasury decides whether to execute them and reports what was actually done. This documentation does not commit a share of net revenue, a buyback formula, or a schedule.

Customer storage charges are not a published treasury allocation, and serving a storage request does not execute treasury policy. This documentation does not claim that automated treasury execution is deployed.

## How LovePIPE Stakers Participate

LovePIPE is the staking path used for Lattice Firestarter eligibility. It represents a proportional claim on PIPE held in the pool. A node operator participates through their LovePIPE holdings on the same basis as other stakers, without receiving a separate node reward.

If treasury later contributes PIPE in a way that increases backing of existing LSTs, that change accrues to all LovePIPE stakers, including those who do not run nodes. LovePIPE is not a promised yield, and backing per LST is not a guaranteed market price.

Deposits and withdrawals use the existing LovePIPE vault. Withdrawal timing follows the vault's current on-chain configuration and is separate from the node's calendar-month qualification period.

## Implementation and References

The storage implementation verifies LovePIPE eligibility and records customer credit usage without creating node earnings.

- [Tokenomics Operations Spec](tokenomics-operations-spec.md): eligibility parameters and implementation boundaries.
- [Parameter registry](tokenomics-params.json): machine-readable protocol values currently documented here.
- [Storage overview](storage/overview.md): customer access and Lattice Firestarter node responsibilities.
- [LovePIPE](https://pipe.love): staking interface for the existing vault.
- [Whitepaper to current mainnet](archive/whitepaper-to-current.md): differences from the archived 2025 publication.
