# Pipe Network Documentation

> **Scope.** This documentation covers Lattice storage, LovePIPE node participation, and related protocol material. Prepaid OpenAI-compatible inference at [pipenetwork.ai](https://pipenetwork.ai) is a separate product and is not documented here.

These pages describe the current mainnet Lattice storage system and how independently operated storage nodes participate. CDN and P1 Overlay appear only as high-level product names; this documentation set does not provide customer APIs, onboarding, or operating guides for them.

**Running a storage node requires 10,000 PIPE staked through LovePIPE. Individual nodes receive no rewards or payouts.** Operators contribute capacity and availability to support the protocol over the long term. Removing node reward obligations supports the protocol's long-term sustainability.

See [Tokenomics](docs/Tokenomics.md) for revenue-funded buybacks and the shared LovePIPE contribution. [Open parameters](docs/Tokenomics.md#open-parameters), including net-revenue allocation and LovePIPE funding treatment, remain unspecified.

## Start Here

- [Welcome](docs/index.md): products and participation.
- [Introduction](docs/getting-started/introduction.md): overview of Pipe Network.
- [Architecture](docs/getting-started/architecture.md): gateways, control plane, storage nodes, and Solana integration.
- [Quickstart](docs/getting-started/quickstart.md): choose customer storage or node participation.
- [Pipe Storage](docs/storage/overview.md): S3-compatible access, customer credits, and storage behavior.
- [Storage API Quickstart](docs/storage/api.md): fund an account, create credentials, and upload an object.

## Storage Nodes

- [Mainnet Storage Nodes](docs/nodes/mainnet.md): requirements, enrollment, and qualification.
- [Wallet and LovePIPE Setup](docs/nodes/wallet-setup.md): node identity and the 10,000 PIPE requirement.
- [Node Operations](docs/nodes/mainnet-operations.md): health, capacity, and troubleshooting.
- [Eligibility Checklist](docs/nodes/mainnet-quality-standards.md): qualification and ongoing participation.
- [Public Node Repository](https://github.com/PipeNetwork/pipe-node): source and release instructions for `lattice-node`.
- [LovePIPE](https://pipe.love): staking, wallet positions, and storage account access.

## Protocol and Economics

- [Tokenomics](docs/Tokenomics.md): no individual node rewards, revenue-funded buybacks, and shared LovePIPE backing.
- [Tokenomics Operations Spec](docs/tokenomics-operations-spec.md): allocation accounting, policy parameters, and implementation boundaries.
- [Network Growth](docs/getting-started/scalability-and-network-growth.md): capacity, coverage, and long-term participation.
- [Performance and Integrity](docs/getting-started/performance-and-fraud-detection.md): storage verification and node eligibility.

## Other Documentation

- [Key Features](docs/getting-started/key-features.md)
- [Opportunities and Use Cases](docs/getting-started/opportunities-and-use-cases.md)
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
