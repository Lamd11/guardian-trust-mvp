# Guardian Trust — On-Chain vs Off-Chain Architecture

## 1. What Does "On-Chain" and "Off-Chain" Mean?

In blockchain systems, data and operations are separated into two categories:

### Off-Chain
Off-chain refers to any data or processing that happens outside the blockchain.

This typically includes:
- Databases
- Application servers
- User interfaces
- File storage (images, PDFs, etc.)
- Private or sensitive data

Off-chain systems are:
- Faster
- More flexible
- Private
- Easier to modify

---

### On-Chain
On-chain refers to data written directly to the blockchain.

This data is:
- Publicly verifiable
- Immutable (cannot be changed)
- Timestamped
- Cryptographically secured

However, on-chain storage is:
- Expensive
- Public
- Limited in capacity
- Not suitable for sensitive data

---

## 2. Real-World Example of On-Chain vs Off-Chain

### Example: NFT Artwork

- The image file (JPEG/PNG) is stored **off-chain** (e.g., on IPFS or cloud storage).
- The blockchain stores a **hash** of the image and a reference link.

Why?

Because:
- The image file is too large for blockchain.
- The blockchain stores proof of ownership and integrity.
- Anyone can verify the hash matches the file.

The blockchain proves authenticity.
The actual content lives off-chain.

---

## 3. Applying This to Guardian Trust

The Guardian Trust system follows the same principle:

We separate:

- Impact data & evidence (off-chain)
- Integrity proof (on-chain)

---

# Off-Chain (CoGs Platform)

The CoGs backend handles:

- User challenge submissions
- Evidence storage (photos, receipts)
- Metadata database
- Impact Record generation
- Storage of blockchain transaction ID (tx_id)

### Off-Chain Stores:

- challenge_id
- primary_sdg
- indicator
- impact_metrics
- evidence_refs (file IDs only)
- timestamp
- pseudonymous_user_id
- tx_id (after anchoring)

### Why Off-Chain?

Because:
- Evidence files contain sensitive information
- Personal identifiers must remain private
- Data needs to be editable during drafting
- Storage must be efficient and scalable

---

# On-Chain (Ethereum Sepolia Testnet)

The blockchain is used strictly as a:

**Tamper-resistant timestamp and integrity layer**

### On-Chain Stores:

- SHA-256 hash of the canonical Impact Record
- Timestamp (via block time)
- Transaction ID (tx_id)

### What Is NEVER Stored On-Chain:

- Names
- Emails
- Photos
- Receipts
- Personal data
- Full JSON records

Only the hash (digital fingerprint) is stored.

---

## 4. How This Demonstrates Trust in Our Project

### Step 1 — User Submits Action (Off-Chain)

A user completes an SDG challenge and submits evidence.

The backend stores:
- Structured data
- Evidence file references

---

### Step 2 — Canonical Impact Record Created (Off-Chain)

The system generates a standardized JSON record.

This ensures:
- Consistent structure
- Reproducible hashing

---

### Step 3 — Hash Generated (Off-Chain)

The JSON is:
- Canonicalized
- Hashed using SHA-256

This produces a unique digital fingerprint.

---

### Step 4 — Hash Anchored On-Chain

The hash is written to Ethereum Sepolia.

This provides:
- Public timestamp
- Immutable proof
- Independent verification

---

### Step 5 — Verification

Later, anyone can:

1. Recompute the hash from the stored record
2. Compare it to the on-chain hash
3. Confirm:
   - ✅ Verified (match)
   - ❌ Tampered (mismatch)
   - ⚠️ Missing (not anchored)

---

## 5. Why This Architecture Matters

This design ensures:

- Privacy is preserved (no personal data on-chain)
- Evidence remains secure and private
- Impact records cannot be secretly altered
- Sponsors and scientists can independently verify integrity
- Trust does not rely on a central authority

Blockchain is not used for speculation or finance.

It is used purely for:

**Integrity. Transparency. Public trust.**

---

## 6. Summary

| Component | Responsibility |
|-----------|----------------|
| Off-Chain | Store data, evidence, metadata |
| On-Chain  | Store cryptographic proof of integrity |
| Verification Layer | Compare computed hash vs anchored hash |

The blockchain acts as a public notary.

The CoGs platform remains the operational system.

Together, they create a trust layer for SDG impact verification.