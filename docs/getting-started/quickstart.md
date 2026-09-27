# Get Started with Pipe

## Use Storage

Open the storage interface at [pipe.love](https://pipe.love/storage), connect your wallet, and purchase prepaid storage credit with USDC. Create credentials for your application and configure an S3-compatible client with the supplied endpoint. Follow the [mainnet storage API quickstart](../storage/api.md) for a complete upload/download example, credential setup, and billing details.

## Run a Lattice Firestarter Node

**You need 10,000 PIPE staked through LovePIPE for each Lattice Firestarter node. Individual nodes receive no rewards or payouts.**

Public mainnet admission is invite-only. Installing `lattice-node` does not enroll a node. There is no public waitlist and no self-serve enrollment form in this repository, and this repository does not publish a public contact channel for requesting invites.

Ordinary public admission requires an invite, the 10,000 PIPE LovePIPE position, and a complete UTC calendar month of passing hourly checks. If you already have an invite and the required position:

1. Prepare a dedicated node identity and its corresponding Solana wallet. The identity helper lives in this documentation repository. A compatible `lattice-node` release (source or binary) is supplied with the invite; this documentation set does not publish a public clone URL.
2. Ensure the wallet holds LovePIPE LSTs representing at least 10,000 underlying PIPE.
3. Use the invite's mesh UUID, trusted HTTPS control-plane URL, and the compatible `lattice-node` release supplied with that invite. Sample values will not enroll a node.
4. Enroll the node, keep it healthy, and retain the required stake through a complete UTC calendar month of finalized hourly checks.
5. Maintain stake, storage integrity, and availability while participating.

Follow [Mainnet Lattice Firestarter Nodes](../nodes/mainnet.md) and [Wallet Setup](../nodes/wallet-setup.md) for details.

## Understand the Contribution Model

See [Tokenomics](../Tokenomics.md) for participation requirements and optional treasury policy.
