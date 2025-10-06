# Testnet

## Setup and Configuration Guide for POP Cache Node on Linux

### 1. System Requirements

#### Recommended specifications:
- 4+ CPU cores
- 16GB+ RAM
- SSD storage with 100GB+ available space
- 1Gbps+ network connection

### 2. Preparing Your System

#### Create a Dedicated User (Optional but Recommended)

```bash
# Switch to root user
sudo su -

# Create a new user 'popcache' with a home directory and bash shell
sudo useradd -m -s /bin/bash popcache

# Add popcache to sudo group
sudo usermod -aG sudo popcache
```

#### Install Required Dependencies

```bash
sudo apt update -y
sudo apt install -y libssl-dev ca-certificates
```

#### Optimize System Settings for Network Performance

The documentation provides a comprehensive set of network performance optimization parameters, including:
- Adjusting local port range
- Increasing maximum connections
- Enabling TCP low latency mode
- Configuring TCP window scaling
- Setting socket buffer sizes

### Configuration Steps

1. **Get an Invite Code**: Register for the node via Airtable link
2. Create configuration directory
3. Download binary
4. Configure `config.json`
5. Create systemd service
6. Configure firewall
7. Set up monitoring

### Key Configuration Tips

- Set memory cache size to 50-70% of total RAM
- Allocate disk cache size leaving 20% free space
- Set workers to match CPU cores
- Provide complete identity configuration
- Include Solana wallet address for rewards

### Important Ports

- HTTP: 80
- HTTPS: 443

### Monitoring

Use built-in endpoints:
- `/state`
- `/metrics`
- `/health`

### Troubleshooting

- Check service logs
- Verify permissions
- Validate configuration
- Check port availability

**Note**: Detailed, step-by-step instructions are provided in the full documentation.