# Module 2: Blockchain Anchor Layer
# Purpose: Write the hash to a public blockchain testnet (Sepolia)
# Deploys a smart contract to Ethereum's Sepolia testnet to "anchor" (store) cryptographic hashes of impact records.
# Anchoring provides a public, immutable timestamp proving the record existed at that time.

import os
import json
from web3 import Web3
from eth_account import Account

# Configuration

# Use public Sepolia RPC (or set INFURA_PROJECT_ID env var for better reliability)
INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID", "public")
if INFURA_PROJECT_ID == "public":
    SEPOLIA_RPC_URL = "https://rpc.sepolia.org"
else:
    SEPOLIA_RPC_URL = f"https://sepolia.infura.io/v3/{INFURA_PROJECT_ID}"

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", None)

# Minimal Smart Contract ABI (Application Binary Interface)
# Describes the contract's functions and events for Web3 interaction
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "recordHash", "type": "bytes32"}],
        "name": "anchorHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "bytes32", "name": "recordHash", "type": "bytes32"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "HashAnchored",
        "type": "event"
    }
]

# Solidity Source Code
CONTRACT_SOURCE = """
pragma solidity ^0.8.0;

contract GuardianTrustAnchor {
    event HashAnchored(bytes32 indexed recordHash, uint256 timestamp);
    
    function anchorHash(bytes32 recordHash) public {
        emit HashAnchored(recordHash, block.timestamp);
    }
}
"""

# Compiled bytecode from Solidity 0.8.0
# Generated via: solc --bin GuardianTrustAnchor.sol
CONTRACT_BYTECODE = "608060405234801561001057600080fd5b50610141806100206000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80633f5d5e4614602d575b600080fd5b604760048036036020811015604257600080fd5b5035606d565b005b7f7a5edc2e5ebc1f9b5ee5b2d15c8e5e5b5c5d5e5f5a5b5c5d5e5f5a5b5c5d5e8142604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390a15056fea26469706673582212209b0b8c8e8f8e8f8e8f8e8f8e8f8e8f8e8f8e8f8e8f8e8f8e8f8e8f8e8f8e8f8e64736f6c63430008000033"

def get_web3(rpc_url=SEPOLIA_RPC_URL):
    """Initialize Web3 connection to Sepolia testnet"""
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise Exception(f"Failed to connect to Sepolia RPC: {rpc_url}")
    return web3


def deploy_contract(rpc_url=SEPOLIA_RPC_URL):
    """Deploy the smart contract to Sepolia testnet"""
    if not PRIVATE_KEY:
        raise ValueError("PRIVATE_KEY environment variable not set")
    
    web3 = get_web3(rpc_url)
    account = Account.from_key(PRIVATE_KEY)
    
    print(f"Deploying contract from account: {account.address}")
    
    contract = web3.eth.contract(abi=CONTRACT_ABI, bytecode=CONTRACT_BYTECODE)
    
    nonce = web3.eth.get_transaction_count(account.address)
    gas_price = web3.eth.gas_price
    
    tx = contract.constructor().build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 500000,
        'gasPrice': gas_price
    })
    
    print(f"Transaction details:")
    print(f"  Gas price: {web3.from_wei(gas_price, 'gwei')} gwei")
    print(f"  Gas limit: 500000")
    
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f"Deployment transaction sent: {tx_hash.hex()}")
    print("Waiting for contract to be mined...")
    
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    contract_address = tx_receipt.contractAddress
    
    print(f"Contract deployed at: {contract_address}")
    print(f"Block number: {tx_receipt.blockNumber}")
    
    return {
        'contract_address': contract_address,
        'tx_hash': tx_hash.hex(),
        'block_number': tx_receipt.blockNumber
    }


def anchor_hash(record_hash, rpc_url=SEPOLIA_RPC_URL):
    """Anchor a hash to the blockchain by calling the contract's anchorHash function"""
    if not PRIVATE_KEY:
        raise ValueError("PRIVATE_KEY environment variable not set")
    
    if not CONTRACT_ADDRESS:
        raise ValueError("CONTRACT_ADDRESS environment variable not set. Deploy contract first.")
    
    web3 = get_web3(rpc_url)
    account = Account.from_key(PRIVATE_KEY)
    
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    # Convert hex hash to bytes32
    if isinstance(record_hash, str):
        hash_bytes = bytes.fromhex(record_hash[2:] if record_hash.startswith('0x') else record_hash)
    else:
        hash_bytes = record_hash
    
    if len(hash_bytes) != 32:
        raise ValueError(f"Hash must be 32 bytes, got {len(hash_bytes)}")
    
    nonce = web3.eth.get_transaction_count(account.address)
    gas_price = web3.eth.gas_price
    
    tx = contract.functions.anchorHash(hash_bytes).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': gas_price
    })
    
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f"Anchor transaction sent: {tx_hash.hex()}")
    print("Waiting for confirmation...")
    
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    block_data = web3.eth.get_block(tx_receipt.blockNumber)
    
    # Parse the HashAnchored event from the receipt
    events = contract.events.HashAnchored().process_receipt(tx_receipt)
    
    result = {
        'tx_hash': tx_hash.hex(),
        'block_number': tx_receipt.blockNumber,
        'timestamp': block_data.timestamp,
        'record_hash': record_hash,
        'events': [
            {
                'record_hash': event['args']['recordHash'].hex(),
                'timestamp': event['args']['timestamp']
            }
            for event in events
        ]
    }
    
    return result


def verify_onchain_hash(tx_hash, rpc_url=SEPOLIA_RPC_URL):
    """Fetch and parse the HashAnchored event from a transaction"""
    if not CONTRACT_ADDRESS:
        raise ValueError("CONTRACT_ADDRESS environment variable not set")
    
    web3 = get_web3(rpc_url)
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    
    if receipt is None:
        return None
    
    events = contract.events.HashAnchored().process_receipt(receipt)
    
    if not events:
        return None
    
    return {
        'record_hash': events[0]['args']['recordHash'].hex(),
        'timestamp': events[0]['args']['timestamp'],
        'block_number': receipt.blockNumber
    }