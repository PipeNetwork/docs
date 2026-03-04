# Mainnet Quality Standards Checklist

Canonical policy version: [Mainnet Tokenomics Policy](../Tokenomics.md) (`v2.6.0`, effective March 3, 2026).
Settlement implementation reference: [Tokenomics Operations Spec](../tokenomics-operations-spec.md) (`v2.6.0`).

All checks are pass/fail for the full `settlement_epoch`.

| Check | Pass Condition | Fail Result |
| --- | --- | --- |
| Stake minimum | Active stake `>= 100 PIPE` in LovePIPE for full settlement_epoch | Node ineligible for full settlement_epoch (`e_i = 0`) |
| Wallet binding | Strict `1:1` binding for full settlement_epoch | Node ineligible for full settlement_epoch (`e_i = 0`) |
| Uptime | `>= 98%` for full settlement_epoch | Node ineligible for full settlement_epoch (`e_i = 0`) |
| Reliability error rate | `< 0.1%` for full settlement_epoch | Node ineligible for full settlement_epoch (`e_i = 0`) |
| Latency | Within healthy band for route class for full settlement_epoch | Node ineligible for full settlement_epoch (`e_i = 0`) |
| CDN cache efficiency | `>= 80%` for CDN workload for full settlement_epoch | Node ineligible for full settlement_epoch (`e_i = 0`) |

Stake link: <https://www.jito.network/restaking/vaults/AoitBUHCmupYA61GrCdXWwU5KqFFVs2fLsAHayywFYRw/>
