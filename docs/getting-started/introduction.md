# Introduction

Pipe Network provides content delivery, distributed object storage, and network routing. Independent operators contribute infrastructure that stores data and brings content closer to users.

## Products

- **Pipe CDN** delivers content through distributed points of presence.
- **Pipe Storage** uses Lattice gateways, a control plane, and storage nodes to provide S3-compatible and native object access.
- **P1 Overlay Network** provides routing across network paths.

## The Current Storage System

Customers purchase prepaid storage credit with USDC on Solana and access objects through a gateway. A central control plane manages enrollment, eligibility, metadata, customer accounting, and storage jobs. The public `lattice-node` software holds object data and serves authorized requests.

Storage uses replication and adaptive layouts, with verified reads and repair across eligible infrastructure. Participation depends on enrollment, LovePIPE ownership, node health, capacity, and the selected storage policy. See [Architecture](architecture.md) and [Pipe Storage](../storage/overview.md).

## Node Participation and Long-Term Sustainability

**Each node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** Operators contribute capacity and availability to the protocol over the long term. Removing recurring node-payment obligations and reward emissions supports protocol sustainability.

The [tokenomics policy](../Tokenomics.md) describes revenue-funded PIPE buyback and burn and the shared LovePIPE contribution. The contribution increases PIPE backing per LST for all stakers, independently of node operation. The final revenue allocation and funding treatment remain to be specified.

Read [Tokenomics](../Tokenomics.md) for the policy or [Quickstart](quickstart.md) to begin.
