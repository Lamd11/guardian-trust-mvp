# Guardian Trust — MVP (Community of Guardians)

Secure Verification of SDG Actions & Contributions  
Blockchain Trust Layer Prototype

---

## 🌍 Project Overview

Guardian Trust is a blockchain-backed integrity layer for the Community of Guardians (CoGs) platform.

Its purpose is simple:

> To prove that sustainability impact records were created at a specific time and have not been altered.

This is **not a cryptocurrency project**.  
This is a trust infrastructure prototype.

The system separates:

- **Off-chain data storage** (evidence, metadata, user submissions)
- **On-chain integrity anchoring** (cryptographic hashes only)

The blockchain acts as a **tamper-resistant public notary**, not a data store.

---

## 🎯 Problem Statement

Impact reporting systems often rely on:

- Self-reported submissions  
- Editable records  
- Centralized databases  
- Trust in platform administrators  

Without independent verification, impact claims can lose credibility.

Guardian Trust solves this by:

- Generating a canonical Impact Record (JSON)
- Hashing the record using SHA-256
- Anchoring the hash to a public blockchain testnet
- Allowing anyone to verify the record has not changed

---

## 🏗 Architecture Overview

### Off-Chain (CoGs Platform)

Responsible for:

- User submissions
- Evidence storage (photos, receipts)
- Metadata database
- Impact Record generation
- Storing blockchain transaction IDs

Stored off-chain:
- Challenge metadata
- SDG indicators
- Impact metrics
- Evidence references (file IDs only)
- Pseudonymous user IDs
- Timestamps
- tx_id (after anchoring)

No personal data is ever written to the blockchain.

---

### On-Chain (Ethereum Sepolia Testnet)

Responsible for:

- Storing SHA-256 hash of canonical Impact Record
- Providing immutable timestamp
- Emitting verification event

Stored on-chain:
- record_hash (bytes32)
- timestamp (via block)
- optional minimal metadata (challenge_number, schema_version)

Never stored on-chain:
- Images
- Names
- Emails
- Receipts
- Raw JSON records

---

## 🔐 Core Trust Flow (MVP)

1. User completes SDG challenge
2. Backend creates canonical Impact Record (JSON)
3. JSON is hashed using SHA-256
4. Hash is anchored to Ethereum Sepolia
5. Transaction ID stored off-chain
6. Verification tool recomputes hash and compares to on-chain value

Verification result:
- ✅ VERIFIED
- ❌ TAMPERED
- ⚠️ MISSING

---

## 📦 Data Objects

### ImpactRecord (Off-Chain)

Canonical JSON object representing:

- Challenge completion
- Impact metrics
- Evidence references
- Timestamp
- Pseudonymous user ID

### AnchorProof (On-Chain)

Blockchain transaction that stores:

- SHA-256 hash of ImpactRecord
- Timestamp
- Optional metadata

### VerificationResult (Off-Chain Tool)

- Recomputed hash
- On-chain hash
- Match status

---

## 🧱 Technical Stack (Planned MVP)

### Backend / Hashing Layer
- Node.js (ethers.js) **or**
- Python (web3.py)

### Blockchain
- Ethereum Sepolia (testnet only)

### Hashing
- SHA-256
- Canonical JSON formatting

### Smart Contract
- Minimal Solidity contract
- Stores hash
- Emits `HashAnchored` event

### Storage (Off-Chain)
- Postgres / SQLite (metadata)
- S3 / Drive equivalent (evidence files)

---

## 🔎 Canonical JSON + Hashing Rules

To ensure reproducibility:

- JSON keys sorted recursively
- UTF-8 encoding
- Compact formatting (no pretty-print)
- ISO-8601 UTC timestamps
- No volatile DB-only fields included

Same record → same hash every time.

---

## 🚧 MVP Scope

This project is:

- A trust prototype
- A student-led build
- A verification layer
- A testnet deployment

This project is NOT:

- Cryptocurrency
- DeFi
- NFT marketplace
- Production blockchain infrastructure
- A financial system

---

## 📌 Roadmap (4 Sprint Model)

**Sprint 1**  
Schema + hashing reproducibility

**Sprint 2**  
Smart contract deployment (testnet) + anchor flow

**Sprint 3**  
Verification tool (CLI or basic UI)

**Sprint 4**  
Demo polish + documentation

---

## 🛡 Privacy & Ethics Guardrails

- No personal identifiers on-chain
- Evidence files remain off-chain
- Use pseudonymous user IDs
- All demo/test data must be fictional
- Blockchain used for integrity — not surveillance or profit

---

## 🧪 Demo Goal

End-to-end demonstration of:

Impact Record → Hash → Blockchain Anchor → Public Verification

The goal is to prove:

> Trust does not rely on the platform alone — it is independently verifiable.

---

## 📂 Repository Status

This repository is a temporary working environment pending official CoGs GitHub organization setup.

It will be migrated once organizational access is available.

---

## 👥 Community of Guardians (CoGs)

Guardian Trust supports the broader CoGs mission:

- SDG Challenge Engine
- Impact Measurement Dashboards
- Science-backed sustainability verification
- Public accountability infrastructure

This project builds one of the core trust pillars of the ecosystem.
