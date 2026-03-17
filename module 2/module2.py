# Module 2: Blockchain Anchor Layer
# Purpose: Write the hash to a public blockchain testnet (Sepolia)
# This module deploys a smart contract to Ethereum's Sepolia testnet and uses it to "anchor" (store) cryptographic hashes of impact records.
# Anchoring provides a public, immutable timestamp proving the record existed at that time.

import os  # For accessing environment variables securely
from web3 import Web3  # Library for interacting with Ethereum blockchain
from eth_account import Account  # For managing Ethereum accounts and signing transactions

# Configuration section: These are the key settings needed to connect and interact with the blockchain


INFURA_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Infura provides access to Ethereum nodes; replace with your project ID
# https://developer.metamask.io/ 
# Confirm with COGS that we have API access on Infura  

PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # Your Ethereum account's private key, stored as an environment variable for security (never hardcode)
CONTRACT_ADDRESS = "0x..."  # The address of the deployed smart contract; initially placeholder, set after deployment

# Minimal Smart Contract ABI (Application Binary Interface)
# This is a JSON description of the contract's functions and events.
# It tells Web3 how to call the contract's methods and listen for events.
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "recordHash", "type": "bytes32"}],  # Function takes one input: a 32-byte hash
        "name": "anchorHash",  # Name of the function
        "outputs": [],  # No return values
        "stateMutability": "nonpayable",  # Function can modify blockchain state (costs gas)
        "type": "function"  # This is a function definition
    },
    {
        "anonymous": False,  # Not an anonymous event
        "inputs": [  # Event parameters
            {"indexed": True, "internalType": "bytes32", "name": "recordHash", "type": "bytes32"},  # Indexed for efficient searching
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}  # Block timestamp when anchored
        ],
        "name": "HashAnchored",  # Event name
        "type": "event"  # This is an event definition
    }
]

# Solidity Contract Source Code (for reference)
# This is the human-readable code of the smart contract written in Solidity.
# You compile this to bytecode using a tool like Remix or solc, then deploy the bytecode.
CONTRACT_SOURCE = """
pragma solidity ^0.8.0;  // Specifies Solidity version

contract GuardianTrustAnchor {  // Contract name
    // Event declaration: Emitted when a hash is anchored, includes the hash and timestamp
    event HashAnchored(bytes32 indexed recordHash, uint256 timestamp);

    // Function to anchor a hash: Takes a bytes32 hash, emits the event with current block timestamp
    function anchorHash(bytes32 recordHash) public {
        emit HashAnchored(recordHash, block.timestamp);  // Emit event with hash and timestamp
    }
}
"""

def get_web3():
    """Initialize Web3 connection to Sepolia testnet"""
    # Create a Web3 instance using Infura's HTTP provider to connect to Sepolia
    web3 = Web3(Web3.HTTPProvider(INFURA_URL))
    # Check if connection is successful
    if not web3.is_connected():
        raise Exception("Failed to connect to Sepolia")  # Raise error if can't connect
    return web3  # Return the Web3 instance for use in other functions


def deploy_contract():
    """Deploy the smart contract to Sepolia testnet"""
    web3 = get_web3()  # Get Web3 connection
    account = Account.from_key(PRIVATE_KEY)  # Create account object from private key

    # Placeholder for compiled bytecode (you get this by compiling the Solidity source)
    bytecode = "0x..."  # Replace with actual bytecode from compiler

    # Create contract object with ABI and bytecode
    contract = web3.eth.contract(abi=CONTRACT_ABI, bytecode=bytecode)

    # Build deployment transaction
    tx = contract.constructor().build_transaction({  # Constructor for deployment
        'from': account.address,  # Your account address
        'nonce': web3.eth.get_transaction_count(account.address),  # Prevent replay attacks
        'gas': 2000000,  # Gas limit for deployment
        'gasPrice': web3.to_wei('20', 'gwei')  # Gas price in gwei
    })

    # Sign the transaction with your private key
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    # Send the signed transaction to the network
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined and get receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Set the global contract address from the receipt
    global CONTRACT_ADDRESS
    CONTRACT_ADDRESS = tx_receipt.contractAddress
    print(f"Contract deployed at: {CONTRACT_ADDRESS}")  # Print for confirmation
    return CONTRACT_ADDRESS  # Return the address

def anchor_hash(record_hash):
    """Anchor a hash to the blockchain by calling the contract's anchorHash function"""
    web3 = get_web3()  # Get Web3 connection
    account = Account.from_key(PRIVATE_KEY)  # Create account object

    # Create contract instance with address and ABI
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

    # Convert the hash string to bytes32 (32 bytes)
    # Remove '0x' prefix if present, then convert hex string to bytes
    hash_bytes = bytes.fromhex(record_hash[2:] if record_hash.startswith('0x') else record_hash)

    # Build the transaction to call anchorHash function
    tx = contract.functions.anchorHash(hash_bytes).build_transaction({
        'from': account.address,  # Your account
        'nonce': web3.eth.get_transaction_count(account.address),  # Unique nonce
        'gas': 100000,  # Gas limit for this call
        'gasPrice': web3.to_wei('20', 'gwei')  # Gas price
    })

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    # Send to network
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for confirmation
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Extract and return key details from the transaction
    result = {
        'tx_hash': tx_hash.hex(),  # Transaction hash as hex string
        'block_number': tx_receipt.blockNumber,  # Block where transaction was included
        'timestamp': web3.eth.get_block(tx_receipt.blockNumber).timestamp  # Timestamp of the block
    }

    return result  # Return the anchoring proof

# Example usage section: How to run the module
if __name__ == "__main__":
    # Uncomment to deploy the contract (do this once)
    # deploy_contract()

    # Example: Anchor a sample hash
    sample_hash = "0x" + "a" * 64  # Dummy 64-character hex hash (32 bytes)
    result = anchor_hash(sample_hash)  # Call the function
    print(result)  # Print the result (tx details)