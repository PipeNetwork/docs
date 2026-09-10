# Pipe Storage

Pipe Storage uses Lattice gateways, a control plane, and distributed storage nodes to store and serve objects. Customers access storage through an S3-compatible API, native HTTP interfaces, or Pipe SDKs. Storage nodes run the public `lattice-node` executable from [PipeNetwork/pipe-node](https://github.com/PipeNetwork/pipe-node).

The service uses prepaid customer credit purchased with USDC on Solana mainnet.

## How Storage Works

| Component | Responsibility |
| --- | --- |
| Gateway/router | Authenticate and serve customer requests, select eligible storage placements, verify data, and coordinate replication and repair. |
| Control plane | Manage enrollment, LovePIPE eligibility, signed topology, metadata, customer credit, and storage jobs in PostgreSQL. |
| Storage node | Persist object data, serve authorized reads and writes, and provide signed receipts and integrity evidence. |

The gateway and control plane coordinate the network. Object payloads are held by storage nodes. A node does not run the control-plane server, customer accounting service, or treasury operations.

Storage supports replication and adaptive layouts. Eligible large immutable objects can move between three full replicas and Reed–Solomon 4+2 erasure coding across distinct approved hosts. Reads verify integrity; repair replaces unavailable replicas or fragments. Conversion depends on fleet health, capacity, observations, and the configured policy. The control plane and gateways remain service availability dependencies.

The standalone node uses persistent local disk by default. The reviewed implementation also supports an optional external S3 payload backend, with local metadata, integrity checks, and backend qualification. Using it requires compatible node and service releases; it is not automatically enabled by having an S3 bucket. Placement considers shared backend failure risks, so offered capacity may not all be assigned.

## Customer Access

Use the [mainnet storage quickstart and API reference](api.md) to fund an account with Solana mainnet USDC, create scoped credentials, and upload an object with AWS CLI or Python. That reference also covers billing, multipart completion, credential rotation, and unsupported S3 features.

Customers use the [storage workspace](https://pipe.love/storage). Customer payments do not create individual node rewards, and customers do not need to operate a node or hold the node's 10,000 PIPE position to use storage.

## Running a Storage Node

**Each node requires 10,000 PIPE staked through LovePIPE, and individual nodes receive no rewards or payouts.** The node wallet must retain LovePIPE LSTs representing at least 10,000 underlying PIPE. Enrollment, a complete calendar month of finalized hourly stake checks, node health, and storage eligibility determine participation.

The [tokenomics policy](../Tokenomics.md) describes revenue-funded PIPE buyback and burn and the shared LovePIPE contribution. The contribution increases PIPE backing per LST for all stakers, independently of node operation. The final revenue allocation and funding treatment remain to be specified.

See [Mainnet Storage Nodes](../nodes/mainnet.md), [Node Operations](../nodes/mainnet-operations.md), and [Tokenomics](../Tokenomics.md) for requirements and the revenue policy.
