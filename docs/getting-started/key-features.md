# Key Features

## Object Storage and Delivery

Pipe Storage supports S3-compatible clients, native HTTP interfaces, and SDKs. Customers use scoped credentials to store and retrieve objects, while gateways coordinate access to distributed storage nodes. Pipe's CDN and routing products support content delivery across the network.

## Customer Usage Accounting

Customers purchase prepaid storage credit with USDC on Solana. The control plane reserves and debits credit for authorized usage and retains accounting evidence. These charges do not create individual node rewards.

## Verification, Replication, and Repair

Nodes serve authorized requests and provide signed receipts and integrity evidence. The storage system supports full replication and adaptive erasure coding, verifies reads, and repairs unavailable replicas or fragments. Placement depends on eligible hosts, capacity, and policy.

Persistent disk is the standalone node's default backend. Compatible releases can qualify an optional external S3 backend, with local metadata and continuing integrity checks.

## LovePIPE Participation

Each storage node requires **10,000 PIPE staked through LovePIPE**, verified through current LST ownership. **There are no individual node rewards or payouts.** Nodes contribute capacity and availability to support the protocol over the long term.

The [tokenomics policy](../Tokenomics.md) describes revenue-funded PIPE buyback and burn and the shared LovePIPE contribution. The contribution increases PIPE backing per LST for all stakers, independently of node operation. The final revenue allocation and funding treatment remain to be specified.

See the [storage guide](../storage/overview.md) for customer access and the [node guide](../nodes/mainnet.md) for participation requirements.
