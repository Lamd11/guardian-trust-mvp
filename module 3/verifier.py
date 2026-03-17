"""
Module 3 — Verification & Demo Layer
Guardian Trust MVP

Purpose:
    Prove that an ImpactRecord has not been altered since it was anchored on-chain.

Usage:
    # Mode A: Live blockchain lookup (requires Module 2 deployed + web3 installed)
    python verifier.py --record record.json --tx 0xabc123...

    # Mode B: Offline / prototype (no blockchain needed)
    python verifier.py --record record.json --hash <expected_hash_hex>

Output:
    VERIFIED  — computed hash matches on-chain hash
    TAMPERED  — hashes differ, record was altered
    MISSING   — no on-chain hash found for this transaction
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from hasher import sha256_hex


# ─────────────────────────────────────────────
# Config — fill these in once Module 2 deploys
# ─────────────────────────────────────────────

SEPOLIA_RPC_URL = "https://rpc.sepolia.org"   # public fallback; prefer Infura/Alchemy
CONTRACT_ADDRESS = None                        # TODO: set after Module 2 deploys to Sepolia
CONTRACT_ABI = None                            # TODO: paste ABI from Module 2 once available


# ─────────────────────────────────────────────
# Blockchain fetch (Mode A)
# ─────────────────────────────────────────────

def fetch_onchain_hash(tx_hash: str, rpc_url: str = SEPOLIA_RPC_URL) -> str | None:
    """
    Fetch the anchored record_hash from a Sepolia transaction receipt.

    Looks for the HashAnchored event emitted by the Module 2 smart contract.

    Returns:
        record_hash as a hex string if found, None if the tx doesn't exist.

    Raises:
        ImportError if web3 is not installed.
        NotImplementedError until Module 2 ABI is available.
    """
    try:
        from web3 import Web3
    except ImportError:
        raise ImportError(
            "web3 is not installed. Run: pip install web3\n"
            "Or use offline mode: --hash <expected_hash_hex>"
        )

    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to Sepolia RPC: {rpc_url}")

    receipt = w3.eth.get_transaction_receipt(tx_hash)

    if receipt is None:
        return None  # tx not found → MISSING

    if CONTRACT_ADDRESS is None or CONTRACT_ABI is None:
        raise NotImplementedError(
            "Module 2 contract not yet deployed.\n"
            "Set CONTRACT_ADDRESS and CONTRACT_ABI in verifier.py once available.\n"
            "For now, use offline mode: --hash <expected_hash_hex>"
        )

    # TODO: parse HashAnchored event once Module 2 ABI is available
    # contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    # events = contract.events.HashAnchored().process_receipt(receipt)
    # return events[0]["args"]["recordHash"].hex()

    raise NotImplementedError("Event parsing not yet implemented — awaiting Module 2 ABI.")


# ─────────────────────────────────────────────
# Core verification logic
# ─────────────────────────────────────────────

def verify(impact_record: dict[str, Any], onchain_hash: str | None) -> dict:
    """
    Recompute hash from record and compare to on-chain value.

    Returns a VerificationResult:
        {
            "computed_hash": str,
            "onchain_hash":  str | None,
            "match":         bool,
            "status":        "VERIFIED" | "TAMPERED" | "MISSING"
        }
    """
    computed = sha256_hex(impact_record)

    if not onchain_hash:
        return {
            "computed_hash": computed,
            "onchain_hash": None,
            "match": False,
            "status": "MISSING",
        }

    # strip 0x prefix if present, normalize case
    onchain_normalized = onchain_hash.lower().removeprefix("0x")
    match = computed.lower() == onchain_normalized

    return {
        "computed_hash": computed,
        "onchain_hash": onchain_normalized,
        "match": match,
        "status": "VERIFIED" if match else "TAMPERED",
    }


# ─────────────────────────────────────────────
# Output
# ─────────────────────────────────────────────

def print_result(result: dict) -> None:
    icons = {"VERIFIED": "[VERIFIED]", "TAMPERED": "[TAMPERED]", "MISSING": "[WARNING]"}
    status = result["status"]

    print()
    print("=" * 54)
    print("  Guardian Trust — Verification Result")
    print("=" * 54)
    print(f"  Status:        {icons.get(status, status)}  {status}")
    print(f"  Computed hash: {result['computed_hash']}")
    print(f"  On-chain hash: {result['onchain_hash'] or 'NOT FOUND'}")

    if status == "MISSING":
        print()
        print("  NOTE: No on-chain anchor was found for this record.")
        print("  This does NOT mean the record was tampered.")
        print("  Possible reasons:")
        print("    - Record was never anchored (Module 2 not run yet)")
        print("    - Wrong tx_hash or hash provided")
        print("    - Transaction is still pending on Sepolia")

    print("=" * 54)
    print()


# ─────────────────────────────────────────────
# CLI entrypoint
# ─────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Guardian Trust — Module 3: Verify an ImpactRecord against its on-chain hash"
    )
    parser.add_argument(
        "--record",
        required=True,
        help="Path to ImpactRecord JSON file",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--tx",
        metavar="TX_HASH",
        help="Sepolia transaction hash (0x...) — fetches on-chain hash via web3",
    )
    group.add_argument(
        "--hash",
        metavar="HEX",
        help="Expected on-chain hash (hex) — offline mode, no blockchain connection needed",
    )

    parser.add_argument(
        "--rpc",
        default=SEPOLIA_RPC_URL,
        help=f"Sepolia RPC URL (default: {SEPOLIA_RPC_URL})",
    )

    args = parser.parse_args()

    with open(args.record) as f:
        record = json.load(f)

    if args.tx:
        print(f"Fetching on-chain hash for tx: {args.tx}")
        onchain_hash = fetch_onchain_hash(args.tx, rpc_url=args.rpc)
    else:
        onchain_hash = args.hash

    result = verify(record, onchain_hash)
    print_result(result)

    # Exit codes: 0 = verified, 1 = tampered, 2 = missing (not necessarily bad)
    exit_codes = {"VERIFIED": 0, "TAMPERED": 1, "MISSING": 2}
    sys.exit(exit_codes.get(result["status"], 1))


if __name__ == "__main__":
    main()
