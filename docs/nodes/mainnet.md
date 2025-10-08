# Mainnet

Coming 2025!

The Pipe Network Mainnet is scheduled to launch in 2025. Stay tuned for more information and updates.

 Running a PipeCDN POP Node

Quick guide to get your CDN node up and running.

## Prerequisites

- **Linux** (Ubuntu 22.04+, Debian 11+)
- **Ports 80 & 443** accessible

## Installation

### Option 1: Pre-built linux Binary

curl -L https://pipe.network/p1-cdn/releases/latest/download/pop -o pop
chmod +x pop

# Configuration

### 1. Set Your Wallet (Required for Earnings)

Create `.env` file or export environment variable:

```bash
export NODE_SOLANA_PUBLIC_KEY="your_solana_wallet_address_here"
```

This is where you'll receive PIPE token rewards for serving traffic.

### 2. Essential Settings

Create `.env` file:

```bash
# Wallet for earnings
NODE_SOLANA_PUBLIC_KEY=your_solana_wallet_address

# Node identity
NODE_NAME=my-pop-node
NODE_EMAIL=operator@example.com
NODE_LOCATION=San Francisco, USA

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

# Ports

### Required Ports

- **80** (HTTP) - Redirects to HTTPS
- **443** (HTTPS) - Main traffic

### Home Networks

If running at home, enable **UPnP** in your router settings. The node will automatically forward ports 80 and 443.

If UPnP doesn't work, manually forward:
- External Port 80 → Your Machine IP:80
- External Port 443 → Your Machine IP:443

### Servers/VPS

Ports should already be accessible. Just ensure firewall allows them:

```bash
# UFW
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# iptables
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### Optional Ports

- **8081** - Health check endpoint
- **9090** - Metrics (Prometheus)

## Running

### Start the Node

```bash
./pop
```

Or with environment file:

```bash
source .env && ./pop
```


# Verification

Check if it's running:

```bash
# Health check
curl http://localhost:8081/health

# Test HTTP
curl -I http://localhost

# Test HTTPS (self-signed cert on first run)
curl -Ik https://localhost
```

## Getting Your Solana Wallet

If you don't have a Solana wallet:

1. **Install Phantom Wallet**: https://phantom.app
2. **Or use Solana CLI**:
   ```bash
   solana-keygen new
   solana address
   ```
3. Copy your public key (starts with letters/numbers, ~44 characters)
4. Add to `.env` as `NODE_SOLANA_PUBLIC_KEY`

⚠️ **Never share your private key/seed phrase!** Only the public key is needed.

## Monitoring

### Check Status

```bash
./pop status           # Node status
./pop earnings         # View earnings
```

### View Metrics

```bash
curl http://localhost:9090/metrics
```

### Check Logs

```bash
# If running directly
./pop 2>&1 | tee pop.log


# Troubleshooting

### Port Already in Use

```bash
sudo lsof -i :80
sudo lsof -i :443
# Kill the process or change ports
```

### UPnP Failed (Home Networks)

1. Enable UPnP in router settings
2. Or manually forward ports 80/443
3. Or disable UPnP: `UPNP_ENABLED=false ./pop`

### Out of Disk Space

Reduce cache size in `.env`:

```bash
DISK_CACHE_SIZE_GB=50
```

### High Memory Usage

Reduce memory cache:

```bash
MEMORY_CACHE_SIZE_MB=256
```

## Performance Tuning

For high-traffic nodes:

```bash
# Increase worker threads
export TOKIO_WORKER_THREADS=16

# Larger cache
export MEMORY_CACHE_SIZE_MB=8192
export DISK_CACHE_SIZE_GB=500

# Use SSD/NVMe for cache
export DISK_CACHE_PATH=/mnt/nvme/cache
```


**That's it!** Your node should now be serving traffic and earning rewards. 🚀

