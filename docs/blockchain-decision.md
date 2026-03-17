# Blockchain Decision — Guardian Trust MVP

## Selected Network: Ethereum Sepolia (Testnet)

For the Guardian Trust MVP, we will use **Ethereum Sepolia** as the blockchain test network.

---

## Why Ethereum Sepolia?

Sepolia was selected because it:

- Is Ethereum’s current long-term supported testnet
- Mirrors Ethereum mainnet behavior (realistic for future scaling)
- Has strong documentation and educational support
- Is compatible with common tools (ethers.js, web3.py)
- Has reliable public blockchain explorers for demo purposes
- Requires no real money (test ETH only)

Most importantly, Sepolia allows us to demonstrate:

**Public verification + immutability + timestamping**  
without financial risk or production complexity.

---

## Why a Testnet (Not Mainnet)?

This is a prototype.

We do not need:
- Real financial transactions
- Production deployment
- Real ETH costs

A testnet allows:
- Safe experimentation
- Free transactions
- Educational use
- Easy iteration

---

## Why Not Other Options?

### ❌ Ethereum Mainnet
- Unnecessary cost
- Real financial exposure
- Not needed for MVP validation

### ❌ Private Blockchain
- Not independently verifiable
- Weakens public trust goal

### ❌ Other Chains (Solana, BSC, etc.)
- Less educational documentation for students
- Unnecessary complexity
- No added trust benefit for this use case

### ❌ Hyperledger / Permissioned Chains
- Centralized governance
- Not publicly verifiable by sponsors or community

---

## Final Position

Ethereum Sepolia is used strictly as a:

**Public, tamper-resistant timestamp and integrity layer**

It is not used for:
- Cryptocurrency
- Tokens
- DeFi
- Financial speculation

The blockchain’s sole purpose in this project is:

**To anchor cryptographic hashes that prove impact records have not been altered.**