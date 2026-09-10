# Welcome to Pipe Network

Pipe Network combines content delivery, distributed object storage, and network routing. The current storage system uses Lattice gateways and a control plane to coordinate independently operated storage nodes.

## Use Pipe

- **Store objects** through the [S3-compatible storage service](storage/overview.md), native HTTP interfaces, or SDKs. Customers purchase prepaid storage credit with USDC on Solana.
- **Deliver content** through Pipe's CDN and routing infrastructure.
- **Contribute storage** by [running a storage node](nodes/mainnet.md), subject to enrollment, stake qualification, and operational requirements.

## Node Participation and LovePIPE

**Each storage node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** The node wallet must hold LSTs representing that underlying PIPE amount and pass the control plane's ownership and qualification checks.

Operators contribute capacity, availability, and resilience to support the protocol over the long term. Removing individual node rewards avoids recurring node-payment obligations and reward emissions.

The [tokenomics policy](Tokenomics.md) describes revenue-funded PIPE buyback and burn and the shared LovePIPE contribution. The contribution increases PIPE backing per LST for all stakers, independently of node operation. The final revenue allocation and funding treatment remain to be specified.

Read [Tokenomics Operations](tokenomics-operations-spec.md) for accounting and implementation details.

## Get Started

- [Quickstart](getting-started/quickstart.md)
- [Storage API Quickstart](storage/api.md)
- [Architecture](getting-started/architecture.md)
- [Mainnet Storage Nodes](nodes/mainnet.md)
- [Node Wallet and LovePIPE](nodes/wallet-setup.md)
- [Node Operations](nodes/mainnet-operations.md)
- [Eligibility Checklist](nodes/mainnet-quality-standards.md)
