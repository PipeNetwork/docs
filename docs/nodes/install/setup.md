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
bash <(curl -sSL https://raw.githubusercontent.com/pipenetwork/docs/main/docs/nodes/install/mainnet.sh)
```
## Monitoring
**View node status and earnings:**
```bash
pop status
pop earnings
```
**Prometheus metrics:**
```bash
curl http://localhost:9090/metrics
```
**Logs ( If use Systemd Service):**
```bash
sudo journalctl -u pipe-node -f
```

## Upgrade Node
```bash
systemctl stop pipe-node
cd /opt/pipe
rm -f pop
curl -L https://pipe.network/p1-cdn/releases/latest/download/pop -o pop
chmod +x pop
systemctl start pipe-node
```
