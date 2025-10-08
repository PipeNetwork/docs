Pipe Network — Tokenomics & Governance (Full Draft v1.0)
Ticker: PIPE
Chain: Solana (SPL token)
Model: Proof‑of‑Useful‑Work (PoUW) for bandwidth & storage; emissions are usage‑gated and follow a disinflation schedule.
Payments: Users can pay in PIPE or burn PIPE to receive usage credits at the oracle price (per‑user burn vaults on Solana).
Staking: Single staking pool; deposit PIPE → receive LovePIPE (non‑rebasing LST).
Governance: Binding votes by PIPE; operator signaling is advisory only.

1) Supply & Genesis Allocation
Total supply at TGE: 1,000,000,000 PIPE.


Allocation (percent of total):


Community : 22% = 220,000,000


Strategic Investors: 32.34% = 323,400,000


Core Contributors & Labs: 15.67% = 156,700,000


Ecosystem & Treasury: 19.99% = 199,900,000


Node Operators: 10% = 100,000,000


UUnlock Schedules: final cliff and linear vesting schedules for each category will be published at or before TGE. Investor tokens unlock 1 year post-TGE; team tokens unlock 2 years post-TGE with a 1-year cliff, followed by linear vesting.

2) Disinflation & Epoch Mint Caps (Nominal)
Annual nominal inflation cap decreases 18% YoY from 12% until it reaches a 1.5% floor.
Formula (plain text):
 r_y = max(1.5%, 12% * 0.82^(y - 1)) where y is the year since launch (1,2,3,…)


Epoch = monthly. For each month in year y:
Monthly cap formula:
 E_cap_month = (r_y / 12) * S_year_start


where S_year_start is circulating supply at the start of that year.
No catch‑up: unused capacity never mints later.
Quick reference (nominal cap, first 12 years):
 Year 1: 12.00% • 2: 9.84% • 3: 8.07% • 4: 6.62% • 5: 5.43% • 6: 4.45% • 7: 3.65% • 8: 2.99% • 9: 2.45% • 10: 2.01% • 11: 1.65% • 12+: 1.50% (floor)

3) Usage‑Gated Emissions (Realized ≤ 0.515 × Cap)
PIPE only mints after verifiable useful work.
Node buckets (gross node pay):
Bandwidth bucket: up to 25% of E_cap_month


Storage bucket: up to 25% of E_cap_month


No cross‑reallocation: if one under‑produces, that share does not mint.


On‑mint: mint 3% of node gross (B_node + S_node) to the treasury each epoch.
Staking commission: 7% of node gross goes to the staking pool (LovePIPE). This is redistribution, not extra mint.
Total minted (max, when both buckets are full):
 Minted_total = (B_node + S_node) + 0.03 * (B_node + S_node)
 Upper bound: Minted_total ≤ 0.515 * E_cap_month
Reference points:
Year 1 nominal = 12% ⇒ max realized ≈ 6.18%


At floor 1.5% ⇒ max realized ≈ 0.7725%



4) Work Pricing & Proofs
USD‑indexed rates (paid in PIPE at oracle price):
Bandwidth: $1 per TB delivered


Storage: $10 per TB‑month held


Proof of bandwidth: signed service receipts with nonces/timestamps; duplicate detection; randomized integrity audits.
Proof of storage: randomized PoR/PoS challenges; integrity checks; eviction penalties.
Quality score: per node q in [0,1] from uptime, latency, audit pass‑rate, correctness.

5) Per‑Epoch Node Payouts
Raw payouts at rate
 B_raw = ($1 * TB_bw) / PIPE_price
 S_raw = ($10 * TBm_st) / PIPE_price


Apply bucket caps
 B_node = min(B_raw, 0.25 * E_cap_month)
 S_node = min(S_raw, 0.25 * E_cap_month)


Staking commission
 staking_to_pool = 0.07 * (B_node + S_node) (nodes receive the rest)


Treasury on‑mint
 Treasury_fee = 0.03 * (B_node + S_node) (additional mint)


Intra‑bucket split (bandwidth or storage):
 R_i,c = [ work_i * q_i * booster_i ] / Σ_j [ work_j * q_j * booster_j ] * C_c
 where C_BW = B_node and C_ST = S_node.
Early Participant Boost: first 12 months. Eligible, well‑performing nodes get booster = 2. Boost only re‑weights within the bucket (no extra mint).

6) Staking & LovePIPE LST
Stake PIPE → receive LovePIPE (non‑rebasing LST).


Yield source: 7% of node gross each epoch accrues to the pool.


Exchange rate: ER = Pool_PIPE / LovePIPE_supply (rises over time).


Deposit: LovePIPE_minted = PIPE_in / ER


Redeem: PIPE_out = LovePIPE * ER


Unbonding/slashing: (e.g., 7–21 days; slashing only if LovePIPE secures critical infra).


Leaderboard (pipe.love): ranks wallets by LovePIPE/staked PIPE (optionally time‑weighted) for future rewards/NFTs.

7) Solana Burn‑to‑Credit
Goal: users can prepay by burning PIPE; credits are recorded in USD at the burn time and then consumed at usage price.
Design: per‑user burn vaults
For each user, derive a program PDA that owns an Associated Token Account (ATA) for the PIPE mint.


Users need a small amount of SOL to fund: (a) rent‑exempt minimum for the ATA, and (b) transaction fees.


Flow (happy path):
dApp derives PDA = find_program_address(["burn", user_pubkey]) and the ATA for (owner = PDA, mint = PIPE).


User funds rent/fees and creates the ATA.


User transfers PIPE to the vault (ATA).


Program executes token::BurnChecked (owner = PDA).


Credit recorded: credit_usd = PIPE_burned * PIPE_price_at_burn (oracle)
 Usage debits: $1/TB bandwidth and $10/TB‑month storage.


Attribution: credit to sender wallet by default (optional signed recipient).
Oracle safety: median/TWAP with deviation clamps; if paused, burns queue until price resumes.
Account lifecycle: PDA may close empty ATAs later to reclaim lamports.
Supply accounting: burns reduce total supply. Public dashboard shows Mint, Burn, Net per epoch (see §13).

8) Node Operator Genesis Program (10% of supply)
Purpose: bootstrap supply side and geo/ISP diversity.
Budget: 100,000,000 PIPE (10% of genesis) over 24 months from mainnet.


Monthly cap: ~4,166,666 PIPE.


Rollover: unspent rolls for up to 3 months, then returns to the Treasury.


Monthly pools (tunable defaults):
Performance (70%) — distributed pro‑rata by points = work * quality * booster; per‑operator cap = 1% of the monthly budget.


Expansion (20%) — bounties for new geos/ISPs; paid on proof of service after probation.


Special (10%) — emergency hotspots & pilots; unused rolls forward.


Eligibility: active in ≥3 of last 4 epochs, pass quality thresholds, not slashed.
Misconduct: forged receipts/fraud → clawback + blacklist.
Note: This program spends from genesis (affects circulating when distributed, not total) and is separate from ongoing PoUW emissions.

10) Oracles, Safety & Anti‑Gaming
Oracle: median/TWAP with deviation clamps; circuit breakers; pause if unhealthy.


Duplicate work: anti‑replay nonces; sampling audits; penalties for duplicates.


Sybil resistance: optional minimum node stake and/or identity attestations for eligibility/boost.


Accounting integrity: per‑epoch Merkle commitments to work/quality roots; verifiable with proofs.



11) Economics & Edge Cases
Under‑utilization: realized mint can fall to zero; no catch‑up.


Price shocks: if PIPE price drops and caps bind, nodes get pro‑rata; Foundation can adjust USD rates, bucket shares, or boost windows.


High burns: sustained burn‑to‑credit offsets emissions; net supply = mint − burn (reported in §13).



13) Public Reporting & Dashboards
Publish the following per epoch (monthly):
S_year_start, r_y, cap_epoch = (r_y / 12) * S_year_start


node_bw_minted, node_st_minted


staking_commission_to_pool = 0.07 * (B_node + S_node)


treasury_on_mint = 0.03 * (B_node + S_node)


mint_total = (B_node + S_node) + treasury_on_mint


Burn log (Solana): list of {burn_vault_pubkey, payer_pubkey, pipe_amount, oracle_price_used, usd_credit, slot, tx_signature}


user_burned_for_credit = sum(pipe_amount)


net_supply_change = mint_total − user_burned_for_credit


Optionals: circulating_delta_from_unlocks, treasury_balance_end, LovePIPE_ER.


Dashboards on pipe.love: /supply, /staking, /treasury, /quality, /votes.

14) Parameter Registry (defaults)
Disinflation: 12% → -18% YoY → 1.5% floor


Epoch: monthly


Buckets (gross): 25% BW and 25% ST of epoch cap (no in‑epoch reallocation)


Treasury on‑mint: 3% of node gross


Staking commission: 7% of node gross → LovePIPE


Rates: $1/TB (BW) and $10/TB‑month (ST) with oracle/TWAP + deviation clamps


Boost: 2x during first 12 months (quality‑gated)


Node‑Op program: 100M PIPE over 24 months; monthly cap ~4.166M; pools 70/20/10 (Performance / Expansion / Special)




16) Disclaimers
This document is informational and not a solicitation. Operators and users must comply with their local laws. Burning tokens is irreversible. This is guidance and meant to allow for flexibility

Symbols (quick reference)
r_y = annual nominal inflation cap for year y


E_cap_month = monthly mint cap = (r_y / 12) * S_year_start


S_year_start = circulating supply at start of the year


B_raw, S_raw = raw bandwidth/storage payouts at USD rates


B_node, S_node = capped node payouts per bucket


Minted_total = (B_node + S_node) + 0.03 * (B_node + S_node)


q = node quality score in [0,1]


booster = multiplier (2 during early‑participant window if eligible)
