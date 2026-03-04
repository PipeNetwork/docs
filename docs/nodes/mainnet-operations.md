# Mainnet Node Operations

Operations reference for running a PipeCDN mainnet node after initial setup.

Setup guide: [Mainnet](mainnet.md)
Canonical policy: [Mainnet Tokenomics Policy](../Tokenomics.md)
Settlement implementation: [Tokenomics Operations Spec](../tokenomics-operations-spec.md)

## 1. Monitoring

Check node status and earnings:

```bash
cd /opt/pipe
./pop status
./pop earnings
```

Prometheus metrics:

```bash
curl http://localhost:9090/metrics
```

Systemd logs:

```bash
journalctl -u pipe -f
```

## 2. Troubleshooting

| Issue | Action |
| --- | --- |
| Port `80`/`443` already in use | `sudo lsof -i :80` and stop conflicting process |
| UPnP failed on home network | Enable UPnP on router or set `UPNP_ENABLED=false` |
| Low disk space | Reduce `DISK_CACHE_SIZE_GB` in `.env` |
| High memory usage | Lower `MEMORY_CACHE_SIZE_MB` (for example `256`) |

## 3. Performance Tuning

For higher traffic:

```bash
export TOKIO_WORKER_THREADS=16
export MEMORY_CACHE_SIZE_MB=8192
export DISK_CACHE_SIZE_GB=500
export DISK_CACHE_PATH=/mnt/nvme/cache
```

Use SSD/NVMe for best cache performance.
