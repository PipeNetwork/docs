# Tokenomics Internal Operations Notes

Aligned with documentation policy `v3.1.1`, updated September 27, 2026.

## Storage Operations

- Monitor finalized hourly LovePIPE ownership checks, complete-month qualification, node health, capacity, and signed receipt integrity.
- Investigate missing or invalid observations and routing exclusions using the recorded evidence. Do not backfill failed qualification hours or reinstate old reward-settlement gates.
- Preserve the distinction between customer credit reservations/debits and node receipts. Accepted receipts create no node earnings.
- Blacklisting stops participation; the control plane does not take custody of or slash LovePIPE positions.
- Historical earnings records in existing Lattice databases remain audit history. They are not a current payout queue.

## Bootstrap Admission Exceptions

Ordinary public mainnet admission requires 10,000 PIPE-equivalent of LovePIPE and a complete qualification month. Lattice also supports a private bootstrap exemption scoped to one enrolled node identity and mesh. It grants minimum placement priority without fabricating ownership snapshots, and creates an immutable grant record and audit event.

An exemption does not bypass lifecycle, heartbeat, endpoint, receipt, integrity, or blacklist checks and creates no node earnings. Revocation removes the exemption and requires ordinary qualification before re-entry. Do not present bootstrap eligibility as evidence that a node passed the normal month of stake checks.

## Treasury Reporting

Public documentation does not commit a percentage of net revenue to buybacks, burns, or LovePIPE backing. Treasury may optionally use protocol revenue to support PIPE and should report only what was actually executed.

If treasury acts in a period, retain:

- Policy version and the actual action taken (buyback, burn, LovePIPE backing, or none).
- Purchase fills, PIPE acquired, execution costs, and unspent balances.
- Burn transactions and confirmed PIPE removed from supply, if any.
- LovePIPE contribution transactions and the corresponding change in backing per LST, if any.

Do not publish `NET_REVENUE_ALLOCATION_PCT`, `LOVEPIPE_ALLOCATION_BPS`, or `LOVEPIPE_FUNDING_TREATMENT` as current policy values. Do not present an intended allocation as a completed transaction. Storage service continues independently of treasury execution; there is no node-payout replay to run.

A contribution that is meant to increase backing of existing LSTs must account for actual vault state. Minting a proportional LST position to the treasury through an ordinary deposit is not sufficient by itself.

## Source Review Boundaries

Reviewed local sources: `lattice-protocol/src/lovepipe.rs`, `lattice-control-plane/src/lovepipe.rs`, and the Lattice guides `LOVEPIPE.md`, `CONTROL_PLANE.md`, `NODE-PAYMENTS-REMOVAL.md`, `ADAPTIVE-STORAGE-IMPLEMENTATION.md`, and `EXTERNAL-S3-STORAGE-IMPLEMENTATION.md`.

The implementation pins eligibility policy `v2.6.0` with a 10,000 PIPE minimum. This documentation update does not change the runtime identifier. Optional treasury actions and automated treasury execution must not be inferred from customer billing or node-payment removal.

The optional external S3 backend is present in the reviewed working tree, whose release guide requires matching node and service releases. Its presence does not establish deployment. Node source and binaries are invite-gated and are provided with the enrollment invite, by Pipe Network operations; this documentation set does not publish a clone URL. Onboarding documentation must follow the selected node release and must not assume an `import-solana-keypair` subcommand exists.
