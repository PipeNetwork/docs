# Mainnet Storage Nodes

Public mainnet node participation requires **10,000 PIPE staked through LovePIPE per node**. Individual nodes receive no rewards or payouts. Operators provide storage, bandwidth, and ongoing availability to support the protocol over the long term.

This guide uses the public `lattice-node` executable on an Ubuntu or Debian host with systemd. Customer storage access is covered in the [storage quickstart](../storage/api.md).

## 1. Obtain Enrollment Settings

Mainnet enrollment is issued by Pipe Network operations. Obtain a one-time invite, mesh UUID, trusted HTTPS control-plane URL, and the compatible node release tag or commit from the network operator before starting the service. The public node cannot issue its own invite. These values are deployment-specific; a sample UUID or token will not enroll a node.

Also prepare a public HTTPS hostname for this node, a reverse proxy forwarding to `127.0.0.1:7101`, and the capacity you intend to contribute. Keep persistent local space for payloads, metadata, and maintenance. The standalone node uses local disk by default.

Prepare and fund the dedicated identity using [Wallet and LovePIPE Setup](wallet-setup.md). The corresponding wallet must hold LSTs representing at least 10,000 underlying PIPE.

## 2. Build and Install

Install Rust 1.88 or newer using your normal Rust toolchain installation. Install the system dependencies and clone the public node repository:

```bash
sudo apt-get update
sudo apt-get install -y build-essential pkg-config libssl-dev git python3 python3-cryptography nginx
git clone https://github.com/PipeNetwork/pipe-node.git
cd pipe-node
read -r -p 'Node release tag or commit supplied with your invite: ' PIPE_NODE_REV
git checkout --detach "$PIPE_NODE_REV"
cargo build --locked --release -p lattice-node
sudo install -m 0755 target/release/lattice-node /usr/local/bin/lattice-node
```

Create a service account and directories for a new installation:

```bash
id pipe-node >/dev/null 2>&1 || sudo useradd --system --home-dir /var/lib/pipe-node --shell /usr/sbin/nologin pipe-node
sudo install -d -o pipe-node -g pipe-node -m 0700 /var/lib/pipe-node
sudo install -d -o root -g root -m 0700 /etc/pipe-node
sudo install -m 0644 deploy/pipe-node.service /etc/systemd/system/pipe-node.service
```

Use the systemd unit from the same node checkout as the binary. Review its memory limits against the host and offered capacity.

## 3. Install the Prepared Identity

Privately transfer the `node.key` prepared in the [wallet guide](wallet-setup.md) to the host. From the documentation checkout on the node host, install it into a new empty data directory:

```bash
read -r -p 'Absolute path to the privately transferred node.key: ' PIPE_NODE_KEY_FILE
sudo python3 docs/scripts/prepare_node_identity.py \
  --node-key "$PIPE_NODE_KEY_FILE" \
  --data-dir /var/lib/pipe-node
sudo chown pipe-node:pipe-node /var/lib/pipe-node/node.key
sudo -u pipe-node /usr/local/bin/lattice-node identity --data-dir /var/lib/pipe-node
```

Compare `lattice_hex` with the public identity recorded when preparing the wallet. Do not continue with a different identity. The installer refuses an existing or populated data directory; preserve it for an existing node instead of initializing it again.

## 4. Configure the Service and Endpoint

Create `/etc/pipe-node/node.env` with `sudoedit /etc/pipe-node/node.env` and restrict it to mode `0600`. Replace all sample values with those supplied for your enrollment:

```dotenv
LATTICE_CONTROL_PLANE_URL=https://control.example
LATTICE_MESH_ID=your-mesh-uuid
LATTICE_ENROLLMENT_TOKEN=your-one-time-invite
LATTICE_DATA_DIR=/var/lib/pipe-node
LATTICE_BIND=127.0.0.1:7101
LATTICE_ENDPOINT=https://node.example
LATTICE_REGION=your-region
```

```bash
sudo chmod 0600 /etc/pipe-node/node.env
```

Capacity is detected from the host by default. To limit the offered local capacity, set `LATTICE_CAPACITY_MB` in this file; the implementation uses MiB-sized units. Leave room for metadata, retained data, and maintenance.

Use `sudoedit /etc/nginx/sites-available/pipe-node` to configure nginx with your node hostname and certificate paths. This example assumes DNS and a trusted TLS certificate are already provisioned:

```nginx
server {
    listen 443 ssl;
    server_name node.example;
    ssl_certificate /etc/ssl/pipe-node/fullchain.pem;
    ssl_certificate_key /etc/ssl/pipe-node/privkey.pem;
    client_max_body_size 0;

    location / {
        proxy_pass http://127.0.0.1:7101;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_request_buffering off;
        proxy_buffering off;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }
}
```

Enable this new site, then check and reload nginx:

```bash
sudo ln -s /etc/nginx/sites-available/pipe-node /etc/nginx/sites-enabled/pipe-node
sudo nginx -t
sudo systemctl reload nginx
```

Allow inbound TCP 443 to the reverse proxy and outbound access to the configured control plane. Keep the node listener on loopback. The advertised hostname must resolve to an endpoint reachable by the network's gateways and health probes.

## 5. Start and Verify

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now pipe-node
sudo systemctl status pipe-node --no-pager
sudo journalctl -u pipe-node -n 100 --no-pager
curl --fail --silent --show-error http://127.0.0.1:7101/health
curl --fail --silent --show-error https://node.example/health
```

The service must report healthy storage and successfully enroll under the expected identity. If the first enrollment response is interrupted, restart with the same invite and identity. After confirmed enrollment, remove `LATTICE_ENROLLMENT_TOKEN` from the environment file; the persistent enrollment state supports subsequent starts.

A healthy endpoint does not mean the node has completed stake qualification. Check the wallet's node status at [LovePIPE](https://pipe.love) and the [eligibility checklist](mainnet-quality-standards.md).

## 6. Qualification and Ongoing Operation

Ordinary mainnet admission requires every finalized hourly LovePIPE ownership check in one complete UTC calendar month to pass. For example, a node enrolled on September 10 that passes every October check can qualify at the November rollover, subject to health and other eligibility checks.

Maintain the required position while active. Dropping below 10,000 PIPE-equivalent or moving the position away causes the next ownership check to fail, removes the node from routing, and requires a new complete valid month for requalification. Narrow bootstrap exceptions are administered separately by the protocol; they do not change the public participation requirement or create node rewards.

Preserve the entire persistent data directory during upgrades. Follow [Node Operations](mainnet-operations.md) for maintenance, repair, and safe retirement. Optional external S3 storage requires a compatible release and backend qualification; configure it for a new or drained instance using the [public node's S3 guide](https://github.com/PipeNetwork/pipe-node/blob/main/lattice-node/S3.md).

Node contributions support the protocol's long-term capacity and resilience. Removing individual reward obligations supports long-term sustainability. The separate shared staking benefit is described in [Tokenomics](../Tokenomics.md).
