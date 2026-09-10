# Mainnet Storage Node Eligibility Checklist

**Public mainnet participation requires at least 10,000 PIPE staked through LovePIPE per node. There are no individual node rewards or payouts.** These checks describe ordinary admission and ongoing routing eligibility.

| Check | Requirement | Effect of Failure |
| --- | --- | --- |
| LovePIPE position | Node wallet owns LSTs representing at least **10,000 underlying PIPE** at each finalized hourly observation. | Observation fails; insufficient ownership removes an active node from routing. |
| Wallet identity | The Solana wallet is the node's persistent identity, with one wallet per node. | A position in another wallet cannot qualify this node. |
| Qualification coverage | Every UTC hour in one complete UTC calendar month has a valid passing observation. | The month does not qualify; a new complete valid month is required. |
| Enrollment | Valid enrollment and authority for the intended control plane and mesh. | Node cannot participate in the mesh. |
| Health and reachability | Node remains reachable, healthy, and able to serve authorized work. | Routing or placement excludes unavailable nodes. |
| Capacity and integrity | Storage meets the selected policy's capacity, verification, and durability requirements. | Affected storage is not eligible for placement or requires repair. |
| Optional external S3 | Compatible release, successful backend qualification and continuing audits. | External capacity remains unavailable or is suspended. |
| Administrative status | Node is enabled and not blacklisted. | Participation stops; unblacklisting and valid qualification are required for re-entry. |

Health and storage checks apply as the service runs. The calendar-month rule applies to LovePIPE qualification; it is not an earnings settlement window. Narrow bootstrap exemptions are administered separately by the protocol and do not change the public requirement or bypass health, integrity, or blacklist checks.

See [Tokenomics](../Tokenomics.md), [Node Operations](mainnet-operations.md), and [LovePIPE](https://pipe.love).
