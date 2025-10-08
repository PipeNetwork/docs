# Mainnet

A quick, clean guide to get your PipeCDN node online and ready for mainnet.

---

## 1. Requirements

**Supported OS**

* Ubuntu 22.04+ or Debian 11+

**Network**

* Open TCP ports: `80` and `443`

**Storage**

* At least 20 GB free space
* SSD/NVMe recommended for cache

---

## 2. Installation

### **Step 1 — Create installation directory**

```bash
cd /opt
mkdir pipe && cd pipe
```

### **Step 2 — Download the latest binary**

```bash
curl -L https://pipe.network/p1-cdn/releases/latest/download/pop -o pop
chmod +x pop
```

> 💡 **Tip:** Keep the binary inside `/opt/pipe` for easy service management and updates.

---

## 3. Configuration

Create a file named `.env` inside `/opt/pipe`:

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

> 💡 **Tip:**  If you run on a VPS, keep `UPNP_ENABLED=false`.
> For home setups, enable it and make sure your router allows UPnP.

---

## 4. Wallet Setup

If you don’t have a Solana wallet yet:

1. Install **[Phantom Wallet](https://phantom.app)**, or
2. Use Solana CLI:

   ```bash
   solana-keygen new
   solana address
   ```
3. Copy your **public key** (44 chars, starts with letters/numbers).
   Paste it into `.env` as `NODE_SOLANA_PUBLIC_KEY`.

> ⚠️ **Never** share your private key or seed phrase.

---

## 5. Run the Node

> Choose **one** of the options below to start your node — pick the method that fits your setup.

### **Option 1 — Manual Run**

Ideal for quick testing or temporary sessions.

```bash
source .env && ./pop
```

### **Option 2 — Background Process**

Run it detached from the terminal (logs to `pop.log`).

```bash
nohup bash -c "source .env && ./pop" > pop.log 2>&1 &
```

### **Option 3 — Systemd Service (Recommended)**

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

> 💡 **Tip:** Systemd ensures auto-restart on crash and starts automatically at boot.


---

## 6. Verification
Check if it's running:

```bash
# Health check
curl http://localhost:8081/health
```

---

## 7. Monitoring

View node status and earnings:

```bash
cd /opt/pipe

./pop status
./pop earnings
```

Prometheus metrics:

```bash
curl http://localhost:9090/metrics
```

Logs ( If use Systemd Service):

```bash
journalctl -u pipe -f
```

---

## 8. Troubleshooting

| Issue                      | Solution                                          |
| -------------------------- | ------------------------------------------------- |
| **Port 80/443 in use**     | `sudo lsof -i :80` → kill conflicting process     |
| **UPnP failed (home use)** | Enable UPnP in router or set `UPNP_ENABLED=false` |
| **Low disk space**         | Reduce `DISK_CACHE_SIZE_GB` in `.env`             |
| **High memory usage**      | Lower `MEMORY_CACHE_SIZE_MB` (e.g. 256)           |

---

## 9. Performance Tuning

For high-traffic setups:

```bash
# Increase worker threads
export TOKIO_WORKER_THREADS=16

# Larger cache
export MEMORY_CACHE_SIZE_MB=8192
export DISK_CACHE_SIZE_GB=500

# Use SSD/NVMe for cache
export DISK_CACHE_PATH=/mnt/nvme/cache
```

Use SSD/NVMe for best caching performance.

---

## 10. Quick Recap

* Download binary -> `chmod +x pop`
* Create `.env`
* Open ports 80 & 443
* Run with `source .env && ./pop`
* Verify with `/health` - the output should return`"status":"healthy"`


Your node is now part of the PipeCDN mesh and ready to earn $PIPE rewards. 🚀

