from __future__ import annotations
import hashlib
import json
from typing import Any

EXCLUDED_FROM_HASH: set[str] = set()


# forces dictionaries to have a consistent key order
def canonicalize(obj: Any) -> Any:
    
    if isinstance(obj, dict):
        sorted_dict = {}
        sorted_keys = sorted(obj.keys())
        
        for key in sorted_keys:
            value = obj[key]
            sorted_dict[key] = canonicalize(value)
        return sorted_dict

    elif isinstance(obj, list):
        new_list = []
        for item in obj:
            new_list.append(canonicalize(item))
        return new_list

    else:
        return obj

### DICTS -> JSON string
def to_canonical_json(record):
    cleaned_record = {}
    for key in record:
        if key not in EXCLUDED_FROM_HASH:
            cleaned_record[key] = record[key]


    sorted_record = canonicalize(cleaned_record)

    json_string = json.dumps(
        sorted_record,
        separators=(",", ":"),  
        ensure_ascii=False      
    )

    return json_string


# hashing using SHA-256 

def sha256_hex(record: dict[str, Any]) -> str:

    json_str = to_canonical_json(record)
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest() # turning strings into bytes to  hash


def sha256_bytes32(record: dict[str, Any]) -> bytes:
    """
    will convert the 64 bytes to 32, so it can be used in smart contract later
    """
    return bytes.fromhex(sha256_hex(record))


# verification helpers 
def verify_hash(record, expected_hash_hex):

    if not record:
        return {
            "computed_hash": "",
            "expected_hash": expected_hash_hex,
            "match": False,
            "status": "EMPTY_RECORD",
        }

    computed_hash = sha256_hex(record)
    hashes_match = computed_hash.lower() == expected_hash_hex.lower()

    if hashes_match:
        status = "VERIFIED"
    else:
        status = "TAMPERED"

    return {
        "computed_hash": computed_hash,
        "expected_hash": expected_hash_hex,
        "match": hashes_match,
        "status": status,
    }

