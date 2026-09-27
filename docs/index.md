# Welcome to Pipe Network

> **Scope.** This documentation covers Pipe Storage, Lattice Firestarter node participation, and related protocol material.

The current storage system uses Lattice gateways and a control plane to coordinate independently operated Lattice Firestarter nodes. CDN and P1 Overlay are high-level product names only in this docs set; customer paths and APIs for those products are not published here.

## Use Pipe

- **Store objects** through the [S3-compatible storage service](storage/overview.md), native HTTP interfaces, or SDKs. Customers purchase prepaid storage credit with USDC on Solana.
- **Contribute storage** by [running a Lattice Firestarter node](nodes/mainnet.md), subject to enrollment, stake qualification, and operational requirements.

## Node Participation and LovePIPE

**Each Lattice Firestarter node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** The node wallet must hold LSTs representing that underlying PIPE amount and pass the control plane's ownership and qualification checks.

Operators contribute capacity, availability, and resilience to support the protocol over the long term. Removing individual node rewards avoids recurring node-payment obligations and reward emissions.

See [Tokenomics](Tokenomics.md) for participation requirements and optional treasury policy.

Read [Tokenomics Operations](tokenomics-operations-spec.md) for eligibility parameters and implementation boundaries.

## Get Started

- [Quickstart](getting-started/quickstart.md)
- [Storage API Quickstart](storage/api.md)
- [Architecture](getting-started/architecture.md)
- [Mainnet Lattice Firestarter Nodes](nodes/mainnet.md)
- [Node Wallet and LovePIPE](nodes/wallet-setup.md)
- [Node Operations](nodes/mainnet-operations.md)
- [Eligibility Checklist](nodes/mainnet-quality-standards.md)
