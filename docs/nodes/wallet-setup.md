# Node Wallet Setup

Use a dedicated Solana wallet address for `NODE_SOLANA_PUBLIC_KEY`.

## 1. Create or Select a Wallet

Option A: Install [Phantom Wallet](https://phantom.app)

Option B: Use Solana CLI:

```bash
solana-keygen new
solana address
```

## 2. Configure Node Wallet

Set the wallet public key in your node `.env` file:

```bash
NODE_SOLANA_PUBLIC_KEY=your_solana_wallet_address
```

## 3. Security Rules

- Never share private keys or seed phrases.
- Use one payout wallet per node (`1:1` binding).
- Do not reuse the same payout wallet across multiple nodes.

## 4. Policy Reference

- Canonical eligibility rules: [Mainnet Tokenomics Policy](../Tokenomics.md)
- Quality checklist: [Mainnet Quality Standards Checklist](mainnet-quality-standards.md)
