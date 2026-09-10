# Storage Node Wallet and LovePIPE

Public mainnet node participation requires a dedicated node wallet holding **LovePIPE LSTs representing at least 10,000 PIPE**. Individual nodes receive no rewards or payouts.

## Prepare the Wallet Locally

The helper below creates compatible wallet and node identity files locally. It makes no network requests, transfers no tokens, and does not enroll a node. It refuses to overwrite existing files or initialize a directory that already contains node data.

Use a trusted machine for wallet preparation. Install Python 3 and its `cryptography` package; on Ubuntu or Debian:

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-cryptography
```

From a checkout of this documentation repository:

```bash
git clone https://github.com/PipeNetwork/docs.git pipe-docs
cd pipe-docs
umask 077
mkdir -p "$HOME/pipe-wallet-backup"
python3 docs/scripts/prepare_node_identity.py \
  --create-keypair "$HOME/pipe-wallet-backup/node-wallet.json" \
  --data-dir "$HOME/pipe-node-identity"
```

The helper prints only `lattice_hex` and `solana_address`, two encodings of the same public key. It saves a Solana JSON keypair at the specified backup path and a hexadecimal `node.key` inside the identity directory. Keep the JSON keypair as private recovery material; it controls the wallet and its LovePIPE position.

To use an existing dedicated Solana JSON keypair instead, choose a new empty output directory:

```bash
python3 docs/scripts/prepare_node_identity.py \
  --keypair /secure/path/node-wallet.json \
  --data-dir "$HOME/pipe-node-identity"
```

The helper validates that the keypair's public key matches its signing seed. A node seed is 32 bytes encoded as 64 hexadecimal characters; the Solana keypair file is a 64-byte JSON array. Wallet tools expecting the JSON format cannot read `node.key` directly.

The [helper source](../scripts/prepare_node_identity.py) is available for review. Download it through `/static/scripts/prepare_node_identity.py` if using the documentation website without a repository checkout.

## Fund the Correct LovePIPE Position

1. Record the helper's `solana_address`. This is the wallet the control plane will check.
2. Deposit PIPE through [LovePIPE](https://pipe.love), or transfer an existing LovePIPE position to that address. You can retain your usual staking wallet and transfer the resulting LSTs to the node wallet.
3. Verify that the node address holds LSTs representing at least **10,000 underlying PIPE** using the finalized vault exchange state. Holding unstaked PIPE alone is insufficient.
4. Keep the position in that wallet throughout qualification and active participation. The node wallet need not have been the original depositor.

| Mainnet account | Address |
| --- | --- |
| LovePIPE vault | `AoitBUHCmupYA61GrCdXWwU5KqFFVs2fLsAHayywFYRw` |
| PIPE mint | `7s9MoSt7VV1J3jVNnw2AyocsQDBdCkPYz5apQDPKy9i5` |
| LovePIPE receipt mint | `CMQdDXbMq63Jv58dfzT27yhB1PZ27Z3yBmuDxVHSZ5tG` |

The minimum is measured in PIPE-equivalent, not a fixed number of LST units. Acquiring or withdrawing a position follows the vault's current on-chain configuration. Vault withdrawal timing is separate from node qualification.

## Install and Verify the Node Identity

Transfer only the prepared `node.key` to the node host through your private file-transfer channel. Preserve the original wallet backup separately. The node host holds a signing seed that can control the wallet, so protect this file and its backups as wallet material.

Follow [Mainnet Storage Nodes](mainnet.md) to install it without overwriting an existing identity. Verify the installed binary prints the same `lattice_hex` before starting enrollment:

```bash
sudo -u pipe-node /usr/local/bin/lattice-node identity --data-dir /var/lib/pipe-node
```

A label or public key written in configuration cannot change the node's signing identity. Do not share one wallet position across multiple nodes.

## Maintain Qualification

Ordinary mainnet admission requires every finalized hourly observation in one complete UTC calendar month to pass. An active node that drops below the minimum is removed from routing and must qualify again through a complete valid month.

LovePIPE stakers participate in the shared revenue contribution independently of node operation. See [Tokenomics](../Tokenomics.md) and the [Eligibility Checklist](mainnet-quality-standards.md).
