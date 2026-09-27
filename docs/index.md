# Welcome to Pipe Network

> **Scope.** This documentation covers Pipe Storage and Lattice Firestarter nodes only. It does not list or document other products.

The current storage system uses Lattice gateways and a control plane to coordinate independently operated Lattice Firestarter nodes. Lattice Firestarter is the product name; nodes run the public `lattice-node` executable from [PipeNetwork/pipe-node](https://github.com/PipeNetwork/pipe-node).

## Use Pipe

- **Store objects** through the [S3-compatible storage service](storage/overview.md), native HTTP interfaces, or SDKs. Customers purchase prepaid storage credit with USDC on Solana.
- **Contribute storage** by [running a Lattice Firestarter node](nodes/mainnet.md), subject to invite-gated enrollment, stake qualification, and operational requirements.

Public Lattice Firestarter admission is invite-only. This repository does not publish a waitlist, a self-serve enrollment form, or a public contact channel for requesting access.

## Node Participation and LovePIPE

**Each Lattice Firestarter node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** The node wallet must hold LSTs representing that underlying PIPE amount and pass the control plane's ownership and qualification checks.

Ordinary public admission is invite-gated, requires the 10,000 PIPE LovePIPE position, and requires a complete UTC calendar month of passing hourly checks. Operators contribute capacity, availability, and resilience to support the protocol over the long term. Removing individual node rewards avoids recurring node-payment obligations and reward emissions.

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
