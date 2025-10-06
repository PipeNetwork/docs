# Pipe Network CDN for Solana Snapshots

## Why Use a Snapshot CDN?

• Save Bandwidth: Reduce large snapshot transfers among validators and RPC providers

• Faster Sync Times: High-performance CDN can saturate 10-20 Gbps connections

• Lower Infrastructure Costs: Reduce operational expenses and improve node uptime

## How It Works

1. **Snapshots Hosted on Pipe Network CDN**
   - Regularly host latest full and incremental Solana Mainnet snapshots

2. **High-Performance snap-fetch**
   - Specialized downloader with multi-threading
   - Parallel chunk downloads to maximize throughput

3. **Solana Validator Auto-Detection**
   - Automatically loads most recent full snapshot
   - Applies incremental snapshots
   - No manual processing required

## Getting Started

### Step 1: Install snap-fetch

```bash
git clone https://github.com/pipenetwork/snap-fetch.git
cd snap-fetch
cargo build --release
```

### Step 2: Download Snapshots

```bash
snap-fetch -o /path/to/ledger/snapshots --skip-existing
```

### Step 3: Start Validator

```bash
solana-validator --ledger /path/to/ledger --snapshot-fetch ...other options
```

## Performance Notes

**Validator Requirements:**
- CPU: 8+ cores
- RAM: 128GB (256GB+ recommended)
- Disk: NVMe SSD, 1TB+ free space
- Network: 10 Gbps+

## Key Benefits

- Potential network-wide bandwidth savings of 3+ petabytes per week
- Improved validator performance
- Reduced operational costs
- Increased network stability

For more details, visit the [GitHub repository](https://github.com/pipenetwork/snap-fetch) or [documentation site](https://docs.pipe.network).