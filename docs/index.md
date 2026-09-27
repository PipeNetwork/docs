# Welcome to Pipe Network

> **Scope.** This documentation covers Pipe Storage and Lattice Firestarter nodes only. It does not list or document other products.

The current storage system uses Lattice gateways and a control plane to coordinate independently operated Lattice Firestarter nodes. Lattice Firestarter is the product name; nodes run the `lattice-node` executable, configured with `LATTICE_*` settings. A compatible `lattice-node` source or binary is provided with the enrollment invite, by Pipe Network operations. This documentation set does not publish a clone URL.

## Use Pipe

- **Store objects** through the [S3-compatible storage service](storage/overview.md) using clients such as AWS CLI or boto3. Customers purchase prepaid storage credit with USDC on Solana. See also the [pipe.love storage docs](https://pipe.love/storage/docs).
- **Contribute storage** by [running a Lattice Firestarter node](nodes/mainnet.md), subject to invite-gated enrollment, stake qualification, and operational requirements.

Public Lattice Firestarter enrollment is invite-only. There is no public waitlist and no self-serve enrollment form. Operators who want to run a node may email [hello@pipe.network](mailto:hello@pipe.network) to inquire. See [Mainnet Lattice Firestarter Nodes](nodes/mainnet.md).

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
