# Introduction

> **Scope.** This documentation covers Pipe Storage and Lattice Firestarter nodes only. It does not name or document other products.

Independent operators run Lattice Firestarter nodes that store object data for the current Lattice storage system. Lattice Firestarter is the product name; the implementation is the `lattice-node` executable, configured with `LATTICE_*` settings. A compatible `lattice-node` source or binary is provided with the enrollment invite, by Pipe Network operations. This documentation set does not publish a clone URL.

## The Current Storage System

**Pipe Storage** uses Lattice gateways, a control plane, and Lattice Firestarter nodes to provide S3-compatible object access. Customers purchase prepaid storage credit with USDC on Solana and access objects through a gateway using S3-compatible clients such as AWS CLI or boto3. Scoped credentials let applications use selected buckets, prefixes, and operations. See the [storage API quickstart](../storage/api.md) and the [pipe.love storage docs](https://pipe.love/storage/docs).

Typical uses include application assets, datasets, media, and other objects. Retrieved objects are served through the documented S3-compatible interface and the storage policy selected for your data. Plan for the availability and performance characteristics of that deployed storage service; this documentation does not publish a separate SLA table.

A central control plane manages enrollment, eligibility, metadata, customer accounting, and storage jobs. Lattice Firestarter nodes hold object data and serve authorized requests. Storage uses replication and adaptive layouts, with verified reads and repair across eligible infrastructure. Participation depends on enrollment, LovePIPE ownership, node health, capacity, and the selected storage policy. See [Architecture](architecture.md) and [Pipe Storage](../storage/overview.md).

## Node Participation and Long-Term Sustainability

**Each Lattice Firestarter node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** Operators contribute capacity and availability to the protocol over the long term. Removing recurring node-payment obligations and reward emissions supports protocol sustainability.

Public mainnet Lattice Firestarter enrollment is invite-only. Ordinary public admission also requires the 10,000 PIPE LovePIPE position and a complete UTC qualification month. Installing node software does not enroll a node. There is no public waitlist and no self-serve enrollment form. Operators who want to run a node may email [hello@pipe.network](mailto:hello@pipe.network) to inquire.

See [Tokenomics](../Tokenomics.md) for participation requirements and optional treasury policy.

Read [Tokenomics](../Tokenomics.md) for the policy or [Quickstart](quickstart.md) to begin.
