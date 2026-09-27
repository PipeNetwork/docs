# Whitepaper to Current Mainnet

The [2025 PIPE Token Whitepaper](pipe-token-whitepaper-2025.pdf) is an archived MiCA notification dated September 3, 2025. It is not the current mainnet operating guide. This page records the differences that matter for readers of this documentation set.

## What the archived PDF described

The summary and crypto-asset functionality sections (including pages 11 and 48) describe a permissionless point-of-presence (PoP) network in which:

- Customers access bandwidth and storage by converting PIPE into non-transferable Data Credits that are burned on use.
- PoP operators stake or receive delegated tokens to become eligible for service provision **and incentives**.
- Token holders can participate in on-chain governance of network upgrades and economic parameters.

Those statements belong to the dated publication. They are not current mainnet policy in this repository.

## What this documentation set describes

| Topic | Archived 2025 PDF | Current docs |
| --- | --- | --- |
| Customer credits | Token converted to Data Credits | Prepaid storage credit purchased with USDC on Solana |
| Node software | PoP-era node guides and binaries | Public `lattice-node` from [PipeNetwork/pipe-node](https://github.com/PipeNetwork/pipe-node), configured with `LATTICE_*` settings |
| Node rewards | Participation incentives for PoPs | **Individual nodes receive no rewards or payouts** |
| Participation stake | Token stake or delegation for PoP eligibility | **10,000 PIPE staked through LovePIPE** per node |
| Enrollment | Permissionless PoP participation | Invite-gated enrollment issued by Pipe Network operations |
| Delivery / routing products | Decentralized CDN / streaming framing | High-level names only; this docs set covers Lattice storage, not CDN or P1 customer APIs |
| Inference | Not the subject of the PDF | Prepaid OpenAI-compatible inference at [pipenetwork.ai](https://pipenetwork.ai) is a separate product and is not documented here |

Older PoP-era setup pages, environment names, and reward language are obsolete. Do not follow them for mainnet.

## Where to read current policy

- [Tokenomics](../Tokenomics.md): no individual node rewards, revenue-funded buybacks, and unspecified open parameters.
- [Tokenomics operations spec](../tokenomics-operations-spec.md): parameter registry and implementation boundaries.
- [Pipe Storage](../storage/overview.md) and [Storage API](../storage/api.md): customer access.
- [Mainnet storage nodes](../nodes/mainnet.md): `lattice-node` enrollment and qualification.

The PDF is preserved unchanged. A revised whitepaper has not been provided for this documentation update.
