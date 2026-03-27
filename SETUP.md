# Setup & Usage — Guardian Trust MVP

## Prerequisites

- Python 3.8+
- pip

## Install Dependencies

```bash
pip install web3
```

> All other dependencies (`hashlib`, `json`, `argparse`) are Python standard library.

---

## Run the End-to-End Demo

```bash
python3 demo_end_to_end.py
```

Shows the full trust flow:

- Module 1: Hashes an ImpactRecord (deterministic)
- Module 2: Anchors hash to blockchain (simulated)
- Module 3: Verifies the record (VERIFIED / TAMPERED)

---

## Test Offline Verification

**Test 1 — Valid record (expect: VERIFIED)**

```bash
python3 "module 3/verifier.py" \
    --record "module 3/sample_record.json" \
    --hash "920e9bdf62d801521daf337f6cb974d63e3efdae8400a643f74d47378786cea5"
```

**Test 2 — Tampered record (expect: TAMPERED)**

```bash
python3 "module 3/verifier.py" \
    --record "module 3/sample_record.json" \
    --hash "0000000000000000000000000000000000000000000000000000000000000000"
```

---

## Deploy to Real Sepolia Blockchain

When ready to go live, follow these steps:

**Step 1 — Get test ETH**

Visit [https://sepoliafaucet.com](https://sepoliafaucet.com) and fund your test wallet.

**Step 2 — Set your private key**

```bash
export PRIVATE_KEY="0x..."
```

Optionally set an Infura/Alchemy project ID for a more reliable RPC:

```bash
export INFURA_PROJECT_ID="your_project_id"
```

**Step 3 — Deploy the contract**

```bash
python3 -c "from 'module 2'.module2 import deploy_contract; print(deploy_contract())"
```

Note the returned `contract_address`.

**Step 4 — Configure the verifier**

In [module 3/verifier.py](module%203/verifier.py), set:

```python
CONTRACT_ADDRESS = "0x..."   # from deploy output
```

The `CONTRACT_ABI` is already defined in `module 2/module2.py`.

**Step 5 — Run live verification**

```bash
python3 "module 3/verifier.py" --record record.json --tx 0x<tx_hash>
```

---

## File Structure

```
guardian-trust-mvp/
├── demo_end_to_end.py          Full integration demo
├── requirements.txt            Python dependencies
│
├── module1/
│   ├── hash_engine.py          Hash engine (canonicalize + SHA-256)
│   └── impact_record.py        ImpactRecord dataclass
│
├── module 2/
│   └── module2.py              Blockchain anchor (deploy + anchor_hash)
│
├── module 3/
│   ├── verifier.py             Verification CLI
│   ├── sample_record.json      Sample ImpactRecord (original)
│   └── sample_record_tampered.json
│
└── docs/
    ├── architecture.md         System design and module overview
    ├── IMPACT_RECORD_SCHEMA.md ImpactRecord field spec and hashing rules
    ├── on-off-chain.md         On-chain vs off-chain architecture explanation
    └── blockchain-decision.md  Why Ethereum Sepolia
```
