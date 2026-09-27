# Key Features

## Object Storage and Delivery

Pipe Storage supports S3-compatible clients, native HTTP interfaces, and SDKs. Customers use scoped credentials to store and retrieve objects, while gateways coordinate access to Lattice Firestarter nodes. CDN and P1 Overlay are not covered as customer products in this documentation set.

## Customer Usage Accounting

Customers purchase prepaid storage credit with USDC on Solana. The control plane reserves and debits credit for authorized usage and retains accounting evidence. These charges do not create individual node rewards.

## Verification, Replication, and Repair

Nodes serve authorized requests and provide signed receipts and integrity evidence. The storage system supports full replication and adaptive erasure coding, verifies reads, and repairs unavailable replicas or fragments. Placement depends on eligible hosts, capacity, and policy.

Persistent disk is the standalone node's default backend. Compatible releases can qualify an optional external S3 backend, with local metadata and continuing integrity checks.

## LovePIPE Participation

Each Lattice Firestarter node requires **10,000 PIPE staked through LovePIPE**, verified through current LST ownership. **There are no individual node rewards or payouts.** Nodes contribute capacity and availability to support the protocol over the long term.

Revenue-funded buybacks and the shared LovePIPE contribution are documented in [Tokenomics](../Tokenomics.md). [Open parameters](../Tokenomics.md#open-parameters), including net-revenue allocation and LovePIPE funding treatment, remain unspecified.

See the [storage guide](../storage/overview.md) for customer access and the [node guide](../nodes/mainnet.md) for participation requirements.
