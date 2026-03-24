# ImpactRecord Schema

## Overview

The `ImpactRecord` is the canonical JSON object that represents a completed SDG challenge action. It is created from backend data (`user_challenges` table) and is deterministically hashed to create the on-chain proof.

**Key Principle:** Same record data → same hash every time (deterministic, reproducible)

---

## Field Mapping: Backend → ImpactRecord

| Backend Table | Column | ImpactRecord Field | Type | Notes |
|---|---|---|---|---|
| `user_challenges` | `user_id` | `user_id` | string | Pseudonymous user identifier |
| `user_challenges` | `challenge_id` | `challenge_id` | string | UUID reference to challenge |
| `challenges` | `challenge_number` | `challenge_number` | integer | Human-readable challenge number |
| `challenges` | `title` | `challenge_title` | string | Challenge name |
| `challenge_sdg_mappings` | `sdg_id` | `sdg_id` | string | UUID of primary SDG |
| `sdgs` | `sdg_number` | `sdg_number` | integer | SDG number (1-17) |
| `challenge_sdg_mappings` | `target_id` | `target_id` | string | UUID of SDG target |
| `challenge_sdg_mappings` | `indicator_id` | `indicator_id` | string | UUID of indicator |
| `user_challenges` | `completed_at` | `completed_at` | string (ISO-8601) | UTC timestamp when challenge was marked complete |
| `user_challenges` | `quantity` | `quantity` | float | Measured impact quantity |
| `user_challenges` | `unit` | `unit` | string | Unit of measurement (e.g., "kg_co2e", "liters", "hours") |
| `user_challenges` | `impact_description` | `impact_description` | string | Text description of impact |
| `user_challenges` | `location` | `location` | string | Human-readable location name |
| `user_challenges` | `latitude` | `latitude` | float | Geographic latitude (8 decimals) |
| `user_challenges` | `longitude` | `longitude` | float | Geographic longitude (8 decimals) |
| `user_challenges` | `proof_url` | `proof_url` | string | URL to evidence (never file content) |
| (derived) | (derived) | `evidence_post_ids` | array[string] | Post IDs referenced as evidence |
| `challenges` | `difficulty` | `difficulty` | string | Challenge difficulty (VERY_EASY, EASY, MEDIUM, HARD, VERY_HARD) |
| `challenges` | `points` | `points` | integer | Points awarded for completion |
| (system) | (system) | `schema_version` | string | Version of this schema (e.g., "1.0") |

---

## JSON Schema (Canonical Format)

All fields are **required** when creating an ImpactRecord. Fields are **sorted alphabetically** by key when hashing.

```json
{
  "schema_version": "1.0",
  "user_id": "user_7f92a",
  "challenge_id": "challenge_abc123",
  "challenge_number": 42,
  "challenge_title": "Reduce Carbon Footprint",
  "sdg_id": "sdg_13",
  "sdg_number": 13,
  "target_id": "target_13_1",
  "indicator_id": "indicator_13_1_1",
  "completed_at": "2026-02-10T20:30:00Z",
  "quantity": 12.4,
  "unit": "kg_co2e",
  "impact_description": "Reduced carbon emissions through energy conservation",
  "location": "San Francisco, CA",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "proof_url": "https://example.com/evidence/photo_abc123.jpg",
  "evidence_post_ids": [
    "post_xyz789",
    "post_def456"
  ],
  "difficulty": "MEDIUM",
  "points": 100
}
```

---

## Important Rules

### 1. Canonicalization (for hashing)

- **Keys must be sorted alphabetically** (recursive)
- **Use compact JSON formatting:** `separators=(",", ":")`
- **UTF-8 encoding** required
- **No extra whitespace** (no pretty-printing)

Example canonical form:
```
{"challenge_id":"challenge_abc123","challenge_number":42,"challenge_title":"...","completed_at":"2026-02-10T20:30:00Z",...}
```

### 2. Timestamps

- **Always ISO-8601 UTC format:** `YYYY-MM-DDTHH:MM:SSZ`
- **Never include timezone abbreviations** (e.g., no "PST", no "+00:00")
- **Always use "Z" suffix** to indicate UTC

Example: `2026-02-10T20:30:00Z` ✅  
Example: `2026-02-10T20:30:00+00:00` ❌ (use Z instead)

### 3. Floating-Point Precision

- **Quantity and coordinates stored as floats** but must be **deterministic**
- Backend uses `DECIMAL(10,2)` for quantity and `DECIMAL(10,8)` / `DECIMAL(11,8)` for lat/lon
- Python floats will serialize consistently for these ranges
- **Best practice:** Document the precision limit (e.g., "2 decimal places for quantity, 8 for coordinates")

### 4. Personal Data

**Never include in ImpactRecord:**
- Real names
- Email addresses
- Phone numbers
- Profile pictures
- Account creation timestamps

**Always use:**
- Pseudonymous user IDs (e.g., `user_7f92a`)
- Post IDs instead of post content
- URLs instead of file content
- Evidence references only (IDs, not data)

### 5. Evidence References

- `proof_url` is a single URL string
- `evidence_post_ids` is an array of post IDs
- **Never include the actual image, receipt, or file content**
- URLs and IDs remain stable and don't change if the files are re-uploaded

---

## Hashing Pipeline (Module 1)

```python
record_dict = {
    "challenge_id": "...",
    "user_id": "...",
    ...
}

# Step 1: Canonicalize (sort keys, compact JSON)
canonical_json = canonicalize(record_dict)
# Result: {"challenge_id":"...","difficulty":"...","points":100,...}

# Step 2: Hash with SHA-256
record_hash = compute_hash(canonical_json)
# Result: "a3f1c2d9e4b7f8c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4"

# This hash is anchored to the blockchain (Module 2)
```

---

## Verification Pipeline (Module 3)

```python
# Given a record and an on-chain hash

# Step 1: Recompute hash using same rules
recomputed_hash = hash_record(record_dict)

# Step 2: Compare to on-chain hash
if recomputed_hash == onchain_hash:
    status = "VERIFIED"  # Record has not been altered
else:
    status = "TAMPERED"  # Record was changed after anchoring

# Step 3: Return result with proof
{
    "recomputed_hash": "a3f1c2d9...",
    "expected_hash": "a3f1c2d9...",
    "status": "VERIFIED"
}
```

---

## Version History

### v1.0 (Current)
- Initial schema based on `user_challenges` table structure
- Aligned with SDG Dashboard backend
- Deterministic hashing with alphabetically sorted keys
- UTF-8 encoding, compact JSON formatting

---

## References

- Backend schema: `schema.sql` (tables: `user_challenges`, `challenges`, `sdgs`, `challenge_sdg_mappings`)
- Module 1 implementation: `module1/impact_record.py` and `module1/hash_engine.py`
- Architecture: `docs/architecture.md`
