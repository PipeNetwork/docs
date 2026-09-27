# Pipe Network Documentation

> **Scope.** This documentation covers Pipe Storage and Lattice Firestarter nodes only. It does not list or document other products.

These pages describe the current mainnet Lattice storage system and how independently operated Lattice Firestarter nodes participate. Lattice Firestarter is the product name; the public node software is the `lattice-node` executable, configured with `LATTICE_*` settings.

**Running a Lattice Firestarter node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** Operators contribute capacity and availability to support the protocol over the long term. Removing node reward obligations supports the protocol's long-term sustainability.

Public mainnet admission is invite-only. Ordinary public admission also requires the 10,000 PIPE LovePIPE position and a complete UTC qualification month. This repository does not publish a waitlist, a self-serve enrollment form, or a public contact channel for requesting access.

See [Tokenomics](docs/Tokenomics.md) for participation requirements and optional treasury policy.

## Start Here

- [Welcome](docs/index.md): scope and participation.
- [Introduction](docs/getting-started/introduction.md): overview of Pipe Storage and Lattice Firestarter.
- [Architecture](docs/getting-started/architecture.md): gateways, control plane, Lattice Firestarter nodes, and Solana integration.
- [Quickstart](docs/getting-started/quickstart.md): choose customer storage or Lattice Firestarter participation.
- [Pipe Storage](docs/storage/overview.md): S3-compatible access, customer credits, and storage behavior.
- [Storage API Quickstart](docs/storage/api.md): fund an account, create credentials, and upload an object.

## Lattice Firestarter Nodes

- [Mainnet Lattice Firestarter Nodes](docs/nodes/mainnet.md): invite-gated enrollment, identity helper, and qualification.
- [Wallet and LovePIPE Setup](docs/nodes/wallet-setup.md): node identity and the 10,000 PIPE requirement.
- [Node Operations](docs/nodes/mainnet-operations.md): health, capacity, and troubleshooting.
- [Eligibility Checklist](docs/nodes/mainnet-quality-standards.md): qualification and ongoing participation.
- [Public Node Repository](https://github.com/PipeNetwork/pipe-node): source and release instructions for the `lattice-node` executable.
- [LovePIPE](https://pipe.love): staking, wallet positions, and storage account access.

## Protocol and Economics

- [Tokenomics](docs/Tokenomics.md): no individual node rewards, LovePIPE staking, and optional treasury policy.
- [Tokenomics Operations Spec](docs/tokenomics-operations-spec.md): eligibility parameters and implementation boundaries.
- [Performance and Integrity](docs/getting-started/performance-and-fraud-detection.md): storage verification and node eligibility.

## Other Documentation

- [Historical Whitepaper](docs/archive/README.md): dated publication, separate from current mainnet policy.
- [Whitepaper to Current Mainnet](docs/archive/whitepaper-to-current.md): what changed versus the archived 2025 PDF.

## Contributing

Submit documentation changes through a pull request. The wallet helper and its tests require Python's `cryptography` package. Run the same checks as CI from the repository root:

```bash
python3 docs/scripts/check_mainnet_docs.py
python3 docs/scripts/check_markdown_links.py
python3 docs/scripts/check_tokenomics_params_sync.py
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo test
```

Run the documentation server locally with `cargo run` and open `http://localhost:3000`. Markdown is rendered under `/docs/`; PDF and JSON links return their original bytes. `/static/` serves raw files from the public documentation tree. Maintainer notes in `internal/` are outside that tree.

Refer to the relevant Pipe Network repositories for license information.

Last updated: September 27, 2026.
