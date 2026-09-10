# Storage Node Operations

Use this guide after [storage-node setup](mainnet.md). Nodes receive no individual rewards or payouts; monitoring focuses on availability, eligibility, capacity, and data integrity.

## Monitoring

Check the node's local health endpoint using its configured bind address:

```bash
curl -fsS http://127.0.0.1:7101/health
```

For installations using the public repository's systemd service, inspect logs with:

```bash
journalctl -u pipe-node -f
```

Monitor disk capacity, local metadata persistence, authorized read/write failures, connectivity to the control plane, and the node's reported lifecycle state. A healthy HTTP endpoint alone does not establish routing or storage eligibility.

Use [LovePIPE](https://pipe.love) to inspect the node wallet's position and available node status. The wallet must hold at least **10,000 PIPE-equivalent of LovePIPE**. Finalized hourly checks, a complete valid calendar month, and healthy storage are required for eligibility. There is no earnings balance or payout export to monitor.

## Troubleshooting

| Issue | Action |
| --- | --- |
| Node remains pending | Check enrollment and the projected qualification date. A partial calendar month does not complete qualification. |
| Stake or ownership check fails | Verify the position is in the wallet corresponding to the node identity and represents at least 10,000 PIPE. Restore the position and allow a complete valid month for requalification. |
| Missing or invalid hourly observation | Have the network operator inspect finalized RPC and qualification evidence. Do not assume current wallet balance repairs missing historical observations. |
| Node health is unavailable | Inspect the service logs, listener, public reverse proxy, and advertised endpoint. |
| Storage capacity is exhausted | Reduce offered capacity or add supported storage while preserving metadata and existing allocations. Allow repair and maintenance headroom. |
| Signed receipt or data verification fails | Preserve logs and storage state for investigation by the network operator. |
| Optional S3 backend remains unqualified | Check compatible releases, backend configuration, credentials, quota, and qualification/audit results. |

## Identity and Maintenance

Preserve `node.key` and the rest of the node's persistent data directory. The identity is also a Solana wallet identity; its seed must be protected. Replacing it changes the identity checked for enrollment and LovePIPE ownership.

Coordinate node retirement, storage migration, and prolonged maintenance with the network operator so stored objects can be repaired or relocated. The optional S3 backend is configured for new or drained storage instances; changing configuration is not an automatic migration of an active store.

Node service receipts remain integrity evidence even though they create no rewards. Blacklisting can stop participation, but the storage control plane does not seize or transfer the operator's LovePIPE position.

Policy reference: [Tokenomics](../Tokenomics.md). Eligibility reference: [Mainnet Eligibility Checklist](mainnet-quality-standards.md).
