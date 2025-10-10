#!/bin/bash

# ========================================
# Interactive setup for Pipe Network Node
# ========================================

echo "========================================"
echo "   Pipe Network POP Node Installation"
echo "========================================"
echo ""

# ---- Collect user input ----
read -p "Enter your Solana wallet address: " SOLANA_WALLET
read -p "Enter your node name: " NODE_NAME
read -p "Enter your contact email: " NODE_EMAIL
read -p "Enter your node location (e.g. Jakarta, Indonesia): " NODE_LOCATION

INSTALL_DIR="/opt/pipe"
SERVICE_NAME="pipe-node"

# ---- Create installation directory ----
sudo mkdir -p $INSTALL_DIR
sudo chown $USER:$USER $INSTALL_DIR
cd $INSTALL_DIR

# ---- Download latest binary ----
echo ""
echo "Downloading latest PipeCDN binary..."
curl -L https://pipe.network/p1-cdn/releases/latest/download/pop -o pop
chmod +x pop

# ---- Create .env file ----
echo ""
echo "Creating .env configuration file..."
cat <<EOF > .env
# Wallet for earnings
NODE_SOLANA_PUBLIC_KEY=$SOLANA_WALLET

# Node identity
NODE_NAME=$NODE_NAME
NODE_EMAIL=$NODE_EMAIL
NODE_LOCATION=$NODE_LOCATION

# Cache configuration (optimized for VPS 24GB RAM / 400GB SSD)
MEMORY_CACHE_SIZE_MB=16384  # 16 GB
DISK_CACHE_SIZE_GB=350      # 350 GB
DISK_CACHE_PATH=./cache

# Network ports
HTTP_PORT=80
HTTPS_PORT=443

# Disable UPnP for VPS
UPNP_ENABLED=false

# Worker threads
TOKIO_WORKER_THREADS=16
EOF

# ---- Create systemd service ----
echo ""
echo "Creating systemd service..."
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
sudo bash -c "cat <<EOF > $SERVICE_FILE
[Unit]
Description=Pipe POP Node
After=network.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/pop
EnvironmentFile=$INSTALL_DIR/.env
Restart=always
RestartSec=10
User=$USER

[Install]
WantedBy=multi-user.target
EOF"

# ---- Enable and start service ----
echo ""
echo "Enabling and starting Pipe Node service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# ---- Final info ----
echo ""
echo "========================================"
echo "✅ PipeCDN node installation completed!"
echo "----------------------------------------"
echo "Service name: $SERVICE_NAME"
echo "Wallet: $SOLANA_WALLET"
echo "Node name: $NODE_NAME"
echo ""
echo "To check node status, run:"
echo "  sudo systemctl status $SERVICE_NAME"
echo ""
echo "To view logs in real-time, run:"
echo "  journalctl -u $SERVICE_NAME -f"
echo "========================================"
