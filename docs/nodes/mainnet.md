# Mainnet

A focused setup guide to install and run your PipeCDN node on mainnet.

Canonical policy version: [Mainnet Tokenomics Policy](../Tokenomics.md) (`v2.6.0`, effective March 3, 2026).
Settlement implementation reference: [Tokenomics Operations Spec](../tokenomics-operations-spec.md) (`v2.6.0`).

---

## 1. Requirements

**Supported OS**

- Ubuntu 24.04+ or Debian 11+

**Network**

- Open TCP ports: `80` and `443`

**Storage**

- At least 20 GB free space
- SSD/NVMe recommended for cache

---

## 2. Installation

### Step 1: Create installation directory

```bash
cd /opt
mkdir pipe && cd pipe
```

### Step 2: Download the latest binary

```bash
curl -L https://pipe.network/p1-cdn/releases/latest/download/pop -o pop
chmod +x pop
```

---

## 3. Configuration

Create `.env` inside `/opt/pipe`:

```bash
# Wallet for earnings
NODE_SOLANA_PUBLIC_KEY=your_solana_wallet_address

# Node identity
NODE_NAME=my-pop-node
NODE_EMAIL="operator@example.com"
NODE_LOCATION="San Francisco, USA"

# Cache configuration
MEMORY_CACHE_SIZE_MB=512
DISK_CACHE_SIZE_GB=100
DISK_CACHE_PATH=./cache

# Network ports
HTTP_PORT=80
HTTPS_PORT=443

# Home network auto port forwarding (disable on VPS/servers)
UPNP_ENABLED=true
```

For VPS or server deployments, set `UPNP_ENABLED=false`.

---

## 4. Wallet Setup

If you do not have a Solana wallet:

1. Install [Phantom Wallet](https://phantom.app), or
2. Use Solana CLI:

```bash
solana-keygen new
solana address
```

Use the public key as `NODE_SOLANA_PUBLIC_KEY` in `.env`.

---

## 5. Run the Node

Choose one method.

### Option 1: Manual run

```bash
source .env && ./pop
```

### Option 2: Background process

```bash
nohup bash -c "source .env && ./pop" > pop.log 2>&1 &
```

### Option 3: Systemd service (recommended)

Create `/etc/systemd/system/pipe.service`:

```ini
[Unit]
Description=Pipe Network POP Node
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=/opt/pipe
ExecStart=/bin/bash -c 'source /opt/pipe/.env && /opt/pipe/pop'
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pipe
sudo systemctl start pipe
sudo journalctl -u pipe -f
```

---

## 6. Verification

```bash
curl http://localhost:8081/health
```

Expected health output includes `"status":"healthy"`.

---

## 7. Next Steps

- Operational monitoring and troubleshooting: [Mainnet Node Operations](mainnet-operations.md)
- Eligibility checklist: [Mainnet Quality Standards Checklist](mainnet-quality-standards.md)
- Canonical policy rules: [Mainnet Tokenomics Policy](../Tokenomics.md)
- Stake into LovePIPE pool: <https://www.jito.network/restaking/vaults/AoitBUHCmupYA61GrCdXWwU5KqFFVs2fLsAHayywFYRw/>
