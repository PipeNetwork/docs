# Pipe Storage

Pipe Storage uses Lattice gateways, a control plane, and Lattice Firestarter nodes to store and serve objects. Customers access storage through an S3-compatible API using clients such as AWS CLI, boto3, or similar S3 tools. Lattice Firestarter nodes run the `lattice-node` executable. A compatible `lattice-node` source or binary is provided with the enrollment invite, by Pipe Network operations. This documentation set does not publish a clone URL.

The service uses prepaid customer credit purchased with USDC on Solana mainnet.

## How Storage Works

| Component | Responsibility |
| --- | --- |
| Gateway/router | Authenticate and serve customer requests, select eligible storage placements, verify data, and coordinate replication and repair. |
| Control plane | Manage enrollment, LovePIPE eligibility, signed topology, metadata, customer credit, and storage jobs in PostgreSQL. |
| Lattice Firestarter node | Persist object data, serve authorized reads and writes, and provide signed receipts and integrity evidence. |

The gateway and control plane coordinate the network. Object payloads are held by Lattice Firestarter nodes. A node does not run the control-plane server, customer accounting service, or treasury operations.

Storage supports replication and adaptive layouts. Eligible large immutable objects can move between three full replicas and Reed–Solomon 4+2 erasure coding across distinct approved hosts. Reads verify integrity; repair replaces unavailable replicas or fragments. Conversion depends on fleet health, capacity, observations, and the configured policy. The control plane and gateways remain service availability dependencies.

The standalone node uses persistent local disk by default. The reviewed implementation also supports an optional external S3 payload backend, with local metadata, integrity checks, and backend qualification. Using it requires a compatible release and the S3 guide shipped with that release or invite package; it is not automatically enabled by having an S3 bucket. Placement considers shared backend failure risks, so offered capacity may not all be assigned.

Nodes add useful capacity, geographic coverage, and availability. Extra offered capacity is not a guarantee of placement. Growth depends on reliable operators, customer demand, and the protocol's ability to place, verify, and repair data.

## Customer Access

Use the [mainnet storage quickstart and API reference](api.md) to fund an account with Solana mainnet USDC, create scoped credentials, and upload an object with AWS CLI or Python. That reference also covers billing, multipart completion, credential rotation, and unsupported S3 features. The [pipe.love storage docs](https://pipe.love/storage/docs) list gateway configuration for the same S3-compatible path.

Customers use the [storage workspace](https://pipe.love/storage). Scoped credentials let applications access selected buckets, prefixes, and operations. Typical uses include application assets, datasets, and media. Plan for the availability and performance of the deployed storage service and the storage policy selected for your data.

Customer payments do not create individual node rewards, and customers do not need to operate a Lattice Firestarter node or hold the node's 10,000 PIPE position to use storage. The control plane reserves and debits prepaid credit for authorized usage and retains accounting evidence.

## Running a Lattice Firestarter Node

**Each Lattice Firestarter node requires 10,000 PIPE staked through LovePIPE, and individual nodes receive no rewards or payouts.** The node wallet must retain LovePIPE LSTs representing at least 10,000 underlying PIPE. Public admission is invite-only. Ordinary public admission also requires a complete calendar month of finalized hourly stake checks, plus node health and storage eligibility.

There is no public waitlist and no self-serve enrollment form. Operators who want to run a node may email [hello@pipe.network](mailto:hello@pipe.network) to inquire. Installing `lattice-node` alone does not enroll a node.

See [Mainnet Lattice Firestarter Nodes](../nodes/mainnet.md), [Node Operations](../nodes/mainnet-operations.md), and [Tokenomics](../Tokenomics.md) for operator requirements and optional treasury policy.
