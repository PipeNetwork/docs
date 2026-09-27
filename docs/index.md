# Welcome to Pipe Network

> **Scope.** This documentation covers Lattice storage, LovePIPE node participation, and related protocol material. Prepaid OpenAI-compatible inference at [pipenetwork.ai](https://pipenetwork.ai) is a separate product and is not documented here.

The current storage system uses Lattice gateways and a control plane to coordinate independently operated storage nodes. CDN and P1 Overlay are high-level product names only in this docs set; customer paths and APIs for those products are not published here.

## Use Pipe

- **Store objects** through the [S3-compatible storage service](storage/overview.md), native HTTP interfaces, or SDKs. Customers purchase prepaid storage credit with USDC on Solana.
- **Contribute storage** by [running a storage node](nodes/mainnet.md), subject to enrollment, stake qualification, and operational requirements.

## Node Participation and LovePIPE

**Each storage node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** The node wallet must hold LSTs representing that underlying PIPE amount and pass the control plane's ownership and qualification checks.

Operators contribute capacity, availability, and resilience to support the protocol over the long term. Removing individual node rewards avoids recurring node-payment obligations and reward emissions.

Revenue-funded buybacks and the shared LovePIPE contribution are documented in [Tokenomics](Tokenomics.md). [Open parameters](Tokenomics.md#open-parameters), including net-revenue allocation and LovePIPE funding treatment, remain unspecified.

Read [Tokenomics Operations](tokenomics-operations-spec.md) for accounting and implementation details.

## Get Started

- [Quickstart](getting-started/quickstart.md)
- [Storage API Quickstart](storage/api.md)
- [Architecture](getting-started/architecture.md)
- [Mainnet Storage Nodes](nodes/mainnet.md)
- [Node Wallet and LovePIPE](nodes/wallet-setup.md)
- [Node Operations](nodes/mainnet-operations.md)
- [Eligibility Checklist](nodes/mainnet-quality-standards.md)
