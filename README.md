# Pipe Network Documentation

Welcome to the official Pipe Network documentation repository. This documentation covers the permissionless full-stack cloud platform that combines content delivery (CDN), Firestarter Storage, and overlay network capabilities.

## 📚 Documentation Structure

### [Welcome](docs/index.md)
Introduction to Pipe Network and its capabilities

### Getting Started
- [Introduction](docs/getting-started/introduction.md) - Overview of Pipe Network architecture and benefits
- [Architecture](docs/getting-started/architecture.md) - Technical architecture and design principles
- [Key Features](docs/getting-started/key-features.md) - Core features and capabilities
- [Scalability and Network Growth](docs/getting-started/scalability-and-network-growth.md) - How Pipe Network scales
- [Opportunities and Use Cases](docs/getting-started/opportunities-and-use-cases.md) - Real-world applications
- [$PIPE Tokenomics](docs/Tokenomics.md) - Token economics and utility
- [Quickstart](docs/getting-started/quickstart.md) - Operating a DevNet CDN PoP Node
- [Performance and Fraud Detection](docs/getting-started/performance-and-fraud-detection.md) - Security measures

### [Pipe Firestarter Storage](docs/pipe-firestarter-storage.md)
Decentralized storage solution with client-side encryption

### Nodes
- [DevNet 2](docs/nodes/devnet-2.md) - DevNet 2 node setup and operation
  - [Troubleshooting](docs/nodes/devnet-2/troubleshooting.md) - Common issues and solutions
- [Testnet](docs/nodes/testnet.md) - Testnet configuration guide
- [Mainnet](docs/nodes/mainnet.md) - Mainnet information (Coming 2025)
- [Workdrop](docs/Workdrop.md) - Workdrop program

### CDN API
- [API Documentation](docs/cdn-api/api-documentation.md) - Complete API reference

### Appendix
- [Pipe Network CDN for Solana Snapshots](docs/appendix/solana-snapshots.md) - Solana validator optimization
- [Old Guardian Node](docs/appendix/old-guardian-node.md) - Legacy Guardian Node information

## 🚀 Quick Links

- [GitHub Repository](https://github.com/PipeNetwork/pipe)
- [Official Website](https://pipe.network)
- [DevNet Form](https://docs.google.com/forms/d/e/1FAIpQLScbxN1qlstpbyU55K5I1UPufzfwshcv7uRJG6aLZQDk52ma0w/viewform)

## 🛠️ Key Components

### Pipe CDN
Hyperlocal content delivery designed for video, gaming, dApps, and AI workloads with sub-10ms latency.

### Firestarter Storage
Decentralized origin storage integrated with delivery, supporting client-side encryption and various storage tiers.

### P1 Overlay Network
Software-defined routing layer that finds the fastest paths across multiple networks.

## 💻 System Requirements

### For PoP Node Operators
- Linux operating system
- Minimum 4GB RAM (16GB+ recommended for production)
- 100GB+ SSD storage
- 1Gbps+ network connection
- 24/7 internet connectivity

## Auto Installations

### Features
- ✅ One-command installation of the Pipe POP Node
- 🔧 Automatically generates a .env configuration file
- 🔥 Opens required firewall ports (80 & 443)
- 🧱 Runs as a persistent systemd service
- 💾 Built-in cache management for improved performance

## 🛠️ Usage

**Download the setup script to your server:**
```bash
wget https://raw.githubusercontent.com/pipenetwork/docs/main/install/auto.sh
nano setup-pop-node.sh
```
**Inside the script, you can customize your node settings in the .env section:**
```bash
NODE_SOLANA_PUBLIC_KEY="your_solana_wallet_address"
NODE_NAME="my-pop-node"
NODE_EMAIL="operator@example.com"
NODE_LOCATION="San Francisco, USA"

MEMORY_CACHE_SIZE_MB=512
DISK_CACHE_SIZE_GB=100
DISK_CACHE_PATH="/root/cache"

HTTP_PORT=80
HTTPS_PORT=443
UPNP_ENABLED=true
```
**Once you’re done editing, make the script executable and run it as root:** 
```bash
chmod +x setup-pop-node.sh
sudo ./setup-pop-node.sh
```



### For Storage Users
- Rust/Cargo for building pipe-cli
- Solana DevNet SOL for transactions

## 📖 Getting Started

1. **New to Pipe Network?** Start with the [Introduction](docs/getting-started/introduction.md)
2. **Want to run a node?** Check out the [DevNet 2 setup guide](docs/nodes/devnet-2.md)
3. **Need storage?** Learn about [Firestarter Storage](docs/pipe-firestarter-storage.md)
4. **Building on Pipe?** Review the [API Documentation](docs/cdn-api/api-documentation.md)

## 🤝 Contributing

This documentation is maintained by the Pipe Network community. If you find any issues or would like to contribute improvements, please submit a pull request or open an issue.

## ⚠️ Important Notes

- **DevNet Warning**: Current implementations run on Solana DevNet. DO NOT USE MAINNET SOL.
- **Mainnet Launch**: Full mainnet is scheduled for 2025
- **Node Registration**: Fill out the [registration form](https://docs.google.com/forms/d/e/1FAIpQLScbxN1qlstpbyU55K5I1UPufzfwshcv7uRJG6aLZQDk52ma0w/viewform) to be notified of updates

### Mica whitepaper
- [Mica whitepaper](docs/mica.pdf)

## 📝 License

Please refer to the official Pipe Network repositories for license information.

---

*Last updated: January 2025*
