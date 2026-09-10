# Tokenomics Internal Operations Notes

Aligned with documentation policy `v3.0.0`, updated September 10, 2026.

## Storage Operations

- Monitor finalized hourly LovePIPE ownership checks, complete-month qualification, node health, capacity, and signed receipt integrity.
- Investigate missing or invalid observations and routing exclusions using the recorded evidence. Do not backfill failed qualification hours or reinstate old reward-settlement gates.
- Preserve the distinction between customer credit reservations/debits and node receipts. Accepted receipts create no node earnings.
- Blacklisting stops participation; the control plane does not take custody of or slash LovePIPE positions.
- Historical earnings records in existing Lattice databases remain audit history. They are not a current payout queue.

## Bootstrap Admission Exceptions

Ordinary public mainnet admission requires 10,000 PIPE-equivalent of LovePIPE and a complete qualification month. Lattice also supports a private bootstrap exemption scoped to one enrolled node identity and mesh. It grants minimum placement priority without fabricating ownership snapshots, and creates an immutable grant record and audit event.

An exemption does not bypass lifecycle, heartbeat, endpoint, receipt, integrity, or blacklist checks and creates no node earnings. Revocation removes the exemption and requires ordinary qualification before re-entry. Do not present bootstrap eligibility as evidence that a node passed the normal month of stake checks.

## Monthly Treasury Reporting

The [operations spec](../docs/tokenomics-operations-spec.md) defines a LovePIPE contribution equal to 7% of the monthly buyback reference amount. The percentage of net revenue and whether the contribution is deducted from or added to that amount remain unspecified.

Before executing the policy, record the net-revenue accounting basis, allocation percentage and effective month, contribution funding treatment, costs, rounding treatment, and pool contribution mechanism. A contribution must benefit existing LST holders; minting a proportional LST position to the treasury through an ordinary deposit is not sufficient by itself.

For each reporting month, retain:

- Policy version and net-revenue calculation, including recognized revenue and deductions.
- Allocation percentage, total allocation, LovePIPE budget, and buyback-and-burn budget.
- Purchase fills, actual PIPE acquired, execution costs, and unspent balances.
- Burn transactions and confirmed PIPE removed from supply.
- LovePIPE contribution transactions and the corresponding change in backing per LST.
- Reconciliation of both destinations to the allocation, with pool contributions excluded from burn totals.

If purchase, burn, or contribution execution is incomplete, report its actual state and remaining balance. Do not present an intended allocation as a completed transaction. Storage service continues independently of treasury execution; there is no node-payout replay to run.

## Source Review Boundaries

Reviewed local sources: `lattice-protocol/src/lovepipe.rs`, `lattice-control-plane/src/lovepipe.rs`, and the Lattice guides `LOVEPIPE.md`, `CONTROL_PLANE.md`, `NODE-PAYMENTS-REMOVAL.md`, `ADAPTIVE-STORAGE-IMPLEMENTATION.md`, and `EXTERNAL-S3-STORAGE-IMPLEMENTATION.md`.

The implementation pins eligibility policy `v2.6.0` with a 10,000 PIPE minimum. This documentation update does not change the runtime identifier. Revenue allocation and automated treasury execution must not be inferred from customer billing or node-payment removal.

The optional external S3 backend is present in the reviewed working tree, whose release guide requires matching public node and private service releases. Its presence does not establish deployment. The public node source also differs from older Lattice identity-import instructions; onboarding documentation must follow the selected node release and must not assume an `import-solana-keypair` subcommand exists.
