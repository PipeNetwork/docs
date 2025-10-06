# DevNet 2

## Pipe PoP Cache Node Documentation

### Overview

Cache Node is a high-performance caching service that helps distribute and serve files efficiently across a network.

### System Requirements

- Linux
- Minimum 4GB RAM (configurable)
- At least 100GB free disk space (configurable)
- 24/7 internet connectivity

> v0.2.6 specifically introduces support for ports 80 and 443, requiring elevated privileges.

### Basic Installation

#### Install

```bash
# download the compiled pop binary
curl -L -o pop "https://dl.pipecdn.app/v0.2.8/pop"
# assign executable permission to pop binary
chmod +x pop
# create folder to be used for download cache
mkdir download_cache
```

#### Quick Start

```bash
sudo ./pop
```

Runs on port 8003, 443 and 80 with 4GB RAM and 100GB disk space.

### Configuration Example

```bash
sudo ./pop \
  --ram 8 \              # RAM in GB
  --max-disk 500 \       # Max disk usage in GB  
  --cache-dir /data \    # Cache location
  --pubKey <KEY>         # Solana public key
```

### Reputation System

The node's reputation score (0-1) is calculated based on three components:

1. **Uptime Score (40%)**: 
   - Grouped by hour
   - Requires 75% daily coverage
   - Weighted by reporting completeness

2. **Historical Score (30%)**: 
   - Based on days with good coverage in last 7 days

3. **Egress Score (30%)**: 
   - Based on total data transferred
   - Normalized against 1TB per day target

### Important Notes

- Maintenance windows under 4 hours don't significantly impact score
- Scores calculated on a rolling 7-day window
- Reputation benefits include priority P2P transfers and referral rewards

### Referral System

- Generate referral code: `./pop --gen-referral-route`
- Sign up with a referral code for benefits