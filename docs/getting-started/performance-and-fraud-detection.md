# Storage Performance and Integrity

Node participation depends on verifiable identity, LovePIPE ownership, healthy storage, and authorized service. These checks protect stored data and customer accounting. **They do not calculate node rewards; individual nodes receive no rewards or payouts.**

## Identity and Ownership

The control plane enrolls persistent node identities and verifies finalized ownership of LovePIPE LSTs representing at least **10,000 PIPE per node**. Fleet-wide hourly observations prevent a transferred position from being counted for both the sending and receiving wallets in the same observation. Every hour of a complete UTC calendar month must pass for qualification.

## Authorized Work and Data Verification

Nodes verify signed authority for storage operations. Gateways verify returned content and integrity evidence. Signed receipts and matching authenticated router reports support usage accounting and investigation; conflicting proofs remain available for review without generating node earnings.

Health checks, capacity admission, replication, adaptive storage policies, and repair help keep data available. Optional external S3 instances require backend qualification and continuing checks; a successful HTTP health response alone does not demonstrate storage readiness.

## Participation Controls

The control plane can exclude unhealthy or ineligible nodes from routing and placement. Administrators can blacklist a node and preserve its evidence for investigation. These actions do not seize, burn, withdraw, or transfer the operator's LovePIPE position.

See [Node Operations](../nodes/mainnet-operations.md) and the [Eligibility Checklist](../nodes/mainnet-quality-standards.md) for the operational requirements.
