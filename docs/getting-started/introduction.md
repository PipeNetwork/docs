# Introduction

> **Scope.** This documentation covers Pipe Storage, Lattice Firestarter node participation, and related protocol material.

Independent operators run Lattice Firestarter nodes that store object data for the current Lattice storage system.

## Products

- **Pipe Storage** uses Lattice gateways, a control plane, and Lattice Firestarter nodes to provide S3-compatible and native object access. That storage service is what this documentation set covers.
- **Pipe CDN** and **P1 Overlay Network** are high-level product names for content delivery and path routing. This documentation set does not describe customer APIs, onboarding, or operations for them.

## The Current Storage System

Customers purchase prepaid storage credit with USDC on Solana and access objects through a gateway. A central control plane manages enrollment, eligibility, metadata, customer accounting, and storage jobs. Lattice Firestarter nodes run the public `lattice-node` executable, which holds object data and serves authorized requests.

Storage uses replication and adaptive layouts, with verified reads and repair across eligible infrastructure. Participation depends on enrollment, LovePIPE ownership, node health, capacity, and the selected storage policy. See [Architecture](architecture.md) and [Pipe Storage](../storage/overview.md).

## Node Participation and Long-Term Sustainability

**Each Lattice Firestarter node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** Operators contribute capacity and availability to the protocol over the long term. Removing recurring node-payment obligations and reward emissions supports protocol sustainability.

Revenue-funded buybacks and the shared LovePIPE contribution are documented in [Tokenomics](../Tokenomics.md). [Open parameters](../Tokenomics.md#open-parameters), including net-revenue allocation and LovePIPE funding treatment, remain unspecified.

Read [Tokenomics](../Tokenomics.md) for the policy or [Quickstart](quickstart.md) to begin.
