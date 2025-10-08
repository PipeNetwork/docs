## Auto Installations

### Features
- ✅ One-command installation of the Pipe POP Node
- 🔧 Automatically generates a .env configuration file
- 🔥 Opens required firewall ports (80 & 443)
- 🧱 Runs as a persistent systemd service
- 💾 Built-in cache management for improved performance

## 🛠️ Usage

**Download the setup script to your server:**
```bash
wget https://raw.githubusercontent.com/pipenetwork/docs/main/install/auto.sh
nano setup-pop-node.sh
```
**Inside the script, you can customize your node settings in the .env section:**
```bash
NODE_SOLANA_PUBLIC_KEY="your_solana_wallet_address"
NODE_NAME="my-pop-node"
NODE_EMAIL="operator@example.com"
NODE_LOCATION="San Francisco, USA"

MEMORY_CACHE_SIZE_MB=512
DISK_CACHE_SIZE_GB=100
DISK_CACHE_PATH="/root/cache"

HTTP_PORT=80
HTTPS_PORT=443
UPNP_ENABLED=true
```
**Once you’re done editing, make the script executable and run it as root:** 
```bash
chmod +x setup-pop-node.sh
sudo ./setup-pop-node.sh
```
