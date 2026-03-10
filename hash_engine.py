import hashlib
import json


def canonicalize(record_dict: dict) -> str:
    """
    Convert a record dictionary to a canonical JSON string.

    Returns a string --- this is what gets hashed.
    """
    return json.dumps(
        record_dict,
        sort_keys=True,       #sort keys recursively 
        separators=(",", ":"),
        ensure_ascii=False,   
    )


def compute_hash(canonical_json: str) -> str:
    """
    Compute the SHA-256 hash of a canonical JSON string.

    Returns a 64-character lowercase hex string.  ("a3f1c2d9e4b7...")

    """
    encoded = canonical_json.encode("utf-8")  
    return hashlib.sha256(encoded).hexdigest()


def hash_record(record_dict: dict) -> dict:
    """
    This is the full pipeline it take a record dict, canonicalize it and then hash it.

    Returns a result dict with:
      - canonical_json: the stable string that was hashed (useful for debugging)
      - record_hash:    the SHA-256 hex digest (this goes on-chain)

    This is the main function Module 2 will call.
    """
    canonical = canonicalize(record_dict)
    record_hash = compute_hash(canonical)

    return {
        "canonical_json": canonical,
        "record_hash": record_hash,
    }


def verify_hash(record_dict: dict, expected_hash: str) -> dict:
    """
    Verify whether a record still matches an expected hash.

    This is what Module 3 will use to verify.

    Returns a result dict with:
      - recomputed_hash: what we computed now
      - expected_hash:   what was stored on-chain
      - status:          VERIFIED | TAMPERED | MISSING
    """
    if not expected_hash:
        return {
            "recomputed_hash": None,
            "expected_hash": None,
            "status": "MISSING",
        }

    result = hash_record(record_dict)
    recomputed = result["record_hash"]
    matched = recomputed == expected_hash.lower()

    return {
        "recomputed_hash": recomputed,
        "expected_hash": expected_hash.lower(),
        "status": "VERIFIED" if matched else "TAMPERED",
    }