# Module 3 — Verification & Demo Layer: Plan

## What It Does

Module 3 is the visible proof engine of Guardian Trust.

Given an ImpactRecord JSON and a blockchain reference, it answers one question:

> Has this record been tampered with since it was anchored on-chain?

**Output states:**

- VERIFIED — computed hash matches on-chain hash. Record is intact.
- TAMPERED — hashes do not match. Record was altered after anchoring.
- MISSING — no on-chain hash found for this record.

---

## Technology Stack

| Component          | Choice                        | Reason                                                            |
|--------------------|-------------------------------|-------------------------------------------------------------------|
| Language           | Python                        | Same as Module 1 (hasher.py). No context switch. Reuse directly. |
| Blockchain client  | web3.py                       | Standard Python Ethereum library, Sepolia-compatible              |
| RPC provider       | Infura or Alchemy (free tier) | Reliable Sepolia access, easy API key setup                       |
| Interface          | CLI (argparse)                | Fast to build, easy to demo, no frontend overhead                 |

> Optional future step: wrap in a Flask/FastAPI endpoint for a simple web UI (Sprint 4).

---

## Core Files

```
guardian-trust-mvp/
├── hasher.py       ← Module 1 (imported by Module 3)
├── verifier.py     ← Module 3 (this module)
└── docs/
    └── module3-plan.md  ← this file
```

---

## Verification Flow

```
Input: ImpactRecord JSON  +  tx_hash (or known hash)
         |
         ▼
Step 1: Recompute SHA-256 using hasher.py (Module 1)
         |
         ▼
Step 2: Fetch anchored hash from Sepolia tx receipt
        → Parse HashAnchored event from Module 2 contract
         |
         ▼
Step 3: Compare computed hash vs on-chain hash
         |
         ▼
Output: VERIFIED / TAMPERED / MISSING
```

---

## Two Operating Modes

### Mode A — Live Blockchain (requires Module 2 deployed)

```bash
python verifier.py --record record.json --tx 0xabc123...
```

- Connects to Sepolia via RPC
- Fetches transaction receipt
- Parses `HashAnchored` event from Module 2 contract
- Compares hashes

### Mode B — Offline / Prototype (no blockchain needed)

```bash
python verifier.py --record record.json --hash <expected_hex>
```

- No blockchain connection required
- Useful for testing before Module 2 is deployed
- Compares computed hash vs a hash passed directly (e.g., one Module 1 produced)
- Fully functional for demo purposes right now

---

## Prototype Strategy (Before Module 2 Exists)

Module 3 can be fully built and tested today using offline mode.

1. Use `hasher.py` (Module 1) to produce a hash from a sample ImpactRecord
2. Pass that hash as `--hash` to `verifier.py`
3. Tamper the record, re-run — should show TAMPERED
4. The blockchain fetch function (`fetch_onchain_hash`) is stubbed with a clear `TODO`
5. Once Module 2 deploys, plug in: contract address + ABI + event parsing

This means Module 3 does not block on Module 2.

---

## Integration with Other Modules

### Module 1 (hasher.py)

- `sha256_hex(record)` imported directly
- Module 3 calls it to recompute the hash for any given ImpactRecord
- The deterministic canonicalization in hasher.py is what makes verification possible

### Module 2 (Blockchain Anchor — not yet built)

- Need from Module 2 once deployed:
  - `CONTRACT_ADDRESS` (Sepolia)
  - Contract ABI (specifically the `HashAnchored` event)
  - Confirmed event signature: `HashAnchored(bytes32 recordHash, uint256 timestamp)`

### CoGs Database (schema.sql)

The `user_challenges` table already has fields that map naturally to Module 3:

| Column               | Module 3 Usage                                      |
|----------------------|-----------------------------------------------------|
| `proof_url`          | Store Sepolia tx explorer URL after anchoring       |
| `verified_by`        | Set to system/automated after Module 3 verifies     |
| `verified_at`        | Timestamp when verification was run                 |
| `verification_notes` | Store "VERIFIED" / "TAMPERED" status + hashes       |

The ImpactRecord JSON maps to CoGs schema fields:
- `challenge_id` → `challenges.challenge_number` + `challenge_sdg_mappings.challenge_code`
- `primary_sdg` → `sdgs.sdg_number`
- `indicator` → `indicators.indicator_number`
- `pseudonymous_user_id` → `users.id` (pseudonymized)

---

## Dependencies

```
web3>=6.0.0
```

Install:
```bash
pip install web3
```

No other new dependencies — `hashlib` and `json` are Python stdlib.

---

## Demo Script (End-to-End, Sprint 4)

1. Load sample ImpactRecord JSON
2. Module 1 produces hash
3. Module 2 anchors hash → returns `tx_hash`
4. Run: `python verifier.py --record record.json --tx <tx_hash>`
5. Output: ✅ VERIFIED

Then to prove tamper detection:

6. Edit one field in the record (e.g., change `impact_metrics.value`)
7. Re-run verifier
8. Output: ❌ TAMPERED

This is the core demo moment.

---

## What Still Needs Module 2

- `CONTRACT_ADDRESS` (Sepolia deployed address)
- Contract ABI (the `HashAnchored` event)
- Confirmed event parameter encoding

All of these slot into the `TODO` section of `verifier.py` once Module 2 is built.
