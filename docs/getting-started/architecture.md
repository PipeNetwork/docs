# Storage Architecture

Pipe's current storage system separates customer gateways, protocol coordination, and Lattice Firestarter nodes holding object data.

## Gateways and Control Plane

Customers use S3-compatible clients through a gateway. The gateway authenticates requests, obtains authorized placements, verifies returned data, and coordinates storage operations.

A central control plane backed by PostgreSQL manages enrollment, node authority, LovePIPE eligibility, signed routing topology, metadata, customer credit, and storage jobs. Gateways and the control plane are service availability dependencies.

## Lattice Firestarter Nodes

The `lattice-node` process stores objects, accepts authorized reads and writes, and provides signed receipts and integrity proofs. Payloads remain on Lattice Firestarter nodes. The control plane and gateways decide placement and coordinate replication, adaptive layouts, and repair.

The standalone node uses persistent disk by default. Compatible releases can also qualify an optional external S3 payload backend while retaining local metadata. Storage policies account for host and shared-backend failures; extra capacity does not guarantee placement.

Adaptive storage can use three full replicas or Reed–Solomon 4+2 fragments across approved hosts. Reads verify integrity before serving data, and retirement of older layouts requires verified replacement data and cleared references. Layout changes depend on the fleet and active policy.

## Capacity and Coverage

Lattice Firestarter nodes add useful capacity, geographic coverage, and availability. Growth depends on reliable operators, customer demand, and the protocol's ability to place, verify, and repair data across eligible infrastructure. Contributing additional capacity does not guarantee that all of it will be used. Operators in underserved regions can improve coverage and resilience without receiving location-based node rewards.

## Solana and LovePIPE

Customer USDC payments purchase prepaid storage credit. The control plane reserves and debits that credit for authorized usage. This accounting does not create node earnings.

Each node must hold LovePIPE LSTs representing at least **10,000 PIPE**. The control plane reads finalized Solana ownership and vault state hourly and requires a complete valid calendar month for qualification. It does not take custody of or transfer those positions.

There are **no individual node rewards or payouts**. Optional treasury actions are described in [Tokenomics](../Tokenomics.md); serving a storage request does not execute treasury policy.
