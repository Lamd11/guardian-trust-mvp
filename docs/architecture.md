# Guardian Trust — System Modules & Architecture (MVP)

This document defines the 3 core modules of the Guardian Trust MVP and how they interact.

The goal is to build a minimal, end-to-end trust engine:

Impact Record → Canonicalize → Hash → Anchor → Verify

Each module can be developed independently and integrated later.

---

# 1. System Overview

Guardian Trust adds a blockchain-backed integrity layer to the Community of Guardians (CoGs) platform.

It does NOT replace the existing backend.

It adds one capability:

> Prove that an impact record existed at a specific time and has not been altered.

The system separates:

- Off-chain: data storage, evidence, metadata
- On-chain: immutable hash anchoring
- Verification layer: integrity comparison

---

# 2. The Three Core Modules

These modules can be developed in parallel.

---

## Module 1 — Impact Record & Hash Engine

### Purpose
Create a deterministic digital fingerprint of a completed SDG action.

### Responsibilities
- Define ImpactRecord JSON schema
- Canonicalize JSON (stable key ordering)
- Normalize timestamps (UTC ISO-8601)
- Compute SHA-256 hash
- Ensure same record → same hash every time

### Output
- `record_hash` (hex string)
- Canonical JSON string (for debug/demo)

This module must be fully deterministic.

If hashing is unstable, verification fails.

---

## Module 2 — Blockchain Anchor Layer

### Purpose
Write the hash to a public blockchain testnet.

### Responsibilities
- Deploy minimal smart contract (Sepolia)
- Implement `anchorHash()` function
- Emit `HashAnchored` event
- Return transaction receipt
- Expose:
  - tx_hash
  - block_number
  - timestamp

### On-Chain Stores
- record_hash (bytes32)
- timestamp (via block)
- optional metadata (challenge_number, schema_version)

No personal data.
No images.
No raw JSON.

This module turns a hash into a public timestamped proof.

---

## Module 3 — Verification & Demo Layer

### Purpose
Prove integrity by comparing computed and on-chain hashes.

### Responsibilities
- Recompute SHA-256 from ImpactRecord
- Fetch on-chain hash (via event or contract read)
- Compare hashes
- Return status:
  - VERIFIED
  - TAMPERED
  - MISSING
- Display output (CLI or simple UI)

This is the visible proof engine.

---

# 3. End-to-End System Flow

Below is the complete MVP flow.

```mermaid
flowchart TD

A[User completes SDG challenge] --> B[CoGs Backend stores submission]
B --> C[Impact Record JSON created]

C --> D[Module 1: Canonicalize JSON]
D --> E[Module 1: SHA-256 Hash]

E --> F[Module 2: Anchor Hash to Sepolia]
F --> G[Blockchain stores hash + timestamp]

G --> H[tx_id returned to backend]

H --> I[tx_id stored off-chain]

I --> J[Module 3: Verification Tool]

C --> J
G --> J

J --> K{Hash Match?}

K -->|Yes| L[VERIFIED]
K -->|No| M[TAMPERED]
K -->|Not Found| N[MISSING]