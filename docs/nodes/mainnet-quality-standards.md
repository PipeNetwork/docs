# Mainnet Quality Standards Checklist

Canonical policy version: [Mainnet Tokenomics Policy](../Tokenomics.md) (`v2.6.0`, effective March 3, 2026).
Settlement implementation reference: [Tokenomics Operations Spec](../tokenomics-operations-spec.md) (`v2.6.0`).

All checks are pass/fail for the full `settlement_epoch`.

| Check | Pass Condition |
| --- | --- |
| Stake minimum | Active stake `>= 100 PIPE` in LovePIPE for full settlement_epoch |
| Wallet binding | Strict `1:1` binding for full settlement_epoch |
| Uptime | `>= 98%` for full settlement_epoch |
| Reliability error rate | `< 0.1%` for full settlement_epoch |
| Latency | Within healthy band for route class for full settlement_epoch |
| CDN cache efficiency | `>= 80%` for CDN workload for full settlement_epoch |

| Rule | Result |
| --- | --- |
| Any check fails in settlement_epoch | Node is ineligible (`e_i = 0`) for that full settlement_epoch |
| No check fails in settlement_epoch | Node remains eligible (`e_i = 1`) |

| Fixed Economics | Value |
| --- | --- |
| CDN payout rate | `$0.25/TB` |
| Storage capacity payout rate | `$0.25/TB-month` |
| Bonus tiers | None |

Stake link: <https://www.jito.network/restaking/vaults/AoitBUHCmupYA61GrCdXWwU5KqFFVs2fLsAHayywFYRw/>
