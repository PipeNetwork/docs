#!/bin/bash

# Pipe Network POP Node Auto-Setup Script
# Official docs: https://docs.pipe.network/docs/nodes/mainnet.md

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
  echo "Please run this script as root."
  exit 1
fi

# Update system and install dependencies
apt update && apt upgrade -y
apt install -y curl ufw

# Option 1: Pre-built Linux Binary
curl -L https://pipe.network/p1-cdn/releases/latest/download/pop -o /usr/local/bin/pop && chmod +x /usr/local/bin/pop

# Create cache directory
mkdir -p /root/cache

# Create .env configuration file
cat <<EOF > /root/.env
# Node Configuration
NODE_SOLANA_PUBLIC_KEY="your_solana_wallet_address"
NODE_NAME="my-pop-node"
NODE_EMAIL="operator@example.com"
NODE_LOCATION="San Francisco, USA"

# Cache settings
MEMORY_CACHE_SIZE_MB=512
DISK_CACHE_SIZE_GB=100
DISK_CACHE_PATH="/root/cache"

# Ports
HTTP_PORT=80
HTTPS_PORT=443

# UPnP
UPNP_ENABLED=true
EOF

# Open required ports
ufw allow 80/tcp
ufw allow 443/tcp

# Create systemd service for the node
cat <<EOF > /etc/systemd/system/pipe-node.service
[Unit]
Description=Pipe Network POP Node
After=network.target

[Service]
EnvironmentFile=/root/.env
ExecStart=/usr/local/bin/pop
WorkingDirectory=/root
Restart=always
RestartSec=5
LimitNOFILE=65536
LimitNPROC=4096
StandardOutput=journal
StandardError=journal
SyslogIdentifier=pipe-node

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable pipe-node
systemctl start pipe-node

echo "Installation complete. Your node is now running as a systemd service."
