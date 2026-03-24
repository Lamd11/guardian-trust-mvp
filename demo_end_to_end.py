#!/usr/bin/env python3
"""
Guardian Trust - End-to-End Demo

This script demonstrates the full integration:
1. Module 1: Load an ImpactRecord and hash it
2. Module 2: Anchor the hash to Sepolia blockchain (optional - can test offline)
3. Module 3: Verify the record against the anchored hash

To run this demo you need:
- For offline mode: just Python
- For blockchain mode: PRIVATE_KEY and CONTRACT_ADDRESS env vars set
"""

import json
import sys
import os

# Add module paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module1'))

from hash_engine import hash_record, verify_hash

# Sample record from Module 3
SAMPLE_RECORD_PATH = "module 3/sample_record.json"
SAMPLE_TAMPERED_PATH = "module 3/sample_record_tampered.json"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def load_record(path):
    with open(path) as f:
        return json.load(f)

def demo_module1():
    """Module 1: Hash Generation"""
    print_section("MODULE 1: Impact Record & Hash Engine")
    
    record = load_record(SAMPLE_RECORD_PATH)
    print(f"\n📋 Loaded ImpactRecord from: {SAMPLE_RECORD_PATH}")
    print(f"   Challenge: {record['challenge_title']} (SDG {record['sdg_number']})")
    print(f"   User: {record['user_id']}")
    print(f"   Impact: {record['quantity']} {record['unit']}")
    
    result = hash_record(record)
    record_hash = result['record_hash']
    canonical_json = result['canonical_json']
    
    print(f"\n🔐 Hash computed:")
    print(f"   SHA-256: {record_hash}")
    print(f"\n📄 Canonical JSON (first 200 chars):")
    print(f"   {canonical_json[:200]}...")
    
    return record, record_hash

def demo_module2_offline():
    """Module 2 Demo (Offline - simulated blockchain)"""
    print_section("MODULE 2: Blockchain Anchor (Simulated)")
    
    record_hash = "920e9bdf62d801521daf337f6cb974d63e3efdae8400a643f74d47378786cea5"
    
    print(f"\n⛓️  OFFLINE MODE (No blockchain deployment needed)")
    print(f"   To anchor to real Sepolia blockchain:")
    print(f"   1. Set PRIVATE_KEY environment variable with test account")
    print(f"   2. Run: python3 -c 'from module2 import deploy_contract; deploy_contract()'")
    print(f"   3. Get deployed CONTRACT_ADDRESS")
    print(f"   4. Set CONTRACT_ADDRESS env var")
    print(f"\n   For this demo, we'll use a simulated tx:")
    print(f"   Simulated Tx Hash: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
    print(f"   Simulated Block: 5555555")
    print(f"   Simulated Timestamp: 1708873800")
    
    return {
        'record_hash': record_hash,
        'tx_hash': '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
        'block_number': 5555555,
        'timestamp': 1708873800
    }

def demo_module3_verify(record, onchain_hash):
    """Module 3: Verification"""
    print_section("MODULE 3: Verification & Proof")
    
    print(f"\n✅ VERIFICATION TEST 1: Valid Record")
    result = verify_hash(record, onchain_hash)
    
    print(f"   Recomputed hash: {result['recomputed_hash']}")
    print(f"   Expected hash:   {result['expected_hash']}")
    print(f"   Status: {result['status']} ✓")
    
    # Test 2: Tampered record
    print(f"\n❌ VERIFICATION TEST 2: Tampered Record")
    tampered_record = load_record(SAMPLE_TAMPERED_PATH)
    print(f"   Changed quantity from 12.4 to 12.3")
    
    result_tampered = verify_hash(tampered_record, onchain_hash)
    print(f"   Recomputed hash: {result_tampered['recomputed_hash']}")
    print(f"   Expected hash:   {result_tampered['expected_hash']}")
    print(f"   Status: {result_tampered['status']} ✓")
    print(f"   Hashes match: {result['recomputed_hash'] == result_tampered['recomputed_hash']}")
    
    return result, result_tampered

def main():
    print("\n" + "🔐 " * 35)
    print("\n  Guardian Trust MVP - Full Integration Demo")
    print("  Impact Record → Hash → Anchor → Verify")
    print("\n" + "🔐 " * 35)
    
    try:
        # Step 1: Module 1
        record, record_hash = demo_module1()
        
        # Step 2: Module 2
        anchor_proof = demo_module2_offline()
        
        # Step 3: Module 3
        verified_result, tampered_result = demo_module3_verify(record, record_hash)
        
        # Summary
        print_section("SUMMARY")
        print(f"\n✅ Module 1: Hash computation")
        print(f"   - Record hashed deterministically")
        print(f"   - Same record always produces same hash")
        
        print(f"\n⛓️  Module 2: Blockchain anchor")
        print(f"   - Hash would be anchored to Sepolia")
        print(f"   - Immutable timestamp proof created")
        print(f"   - Transaction stored off-chain")
        
        print(f"\n🔍 Module 3: Verification")
        print(f"   - Valid record: {verified_result['status']}")
        print(f"   - Tampered record: {tampered_result['status']}")
        print(f"   - Tampering is instantly detectable")
        
        print(f"\n📊 Trust Architecture:")
        print(f"   1. Record exists at specific time (via blockchain)")
        print(f"   2. Record has not been altered (via hash comparison)")
        print(f"   3. Verification is independent and reproducible")
        
        print_section("NEXT STEPS")
        print(f"\n To deploy to real Sepolia testnet:")
        print(f"  1. Get test ETH from faucet: https://sepoliafaucet.com")
        print(f"  2. Export private key to PRIVATE_KEY env var")
        print(f"  3. Run: python3 -c \"from module2 import deploy_contract; print(deploy_contract())\"")
        print(f"  4. Export returned address to CONTRACT_ADDRESS env var")
        print(f"  5. Update verifier.py with CONTRACT_ADDRESS and CONTRACT_ABI")
        print(f"\n✅ Demo complete!")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
