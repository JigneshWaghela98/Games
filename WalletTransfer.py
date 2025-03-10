from web3 import Web3

# Connect to Polygon network via Infura
infura_url = 'https://polygon-mainnet.infura.io/v3/79467c63c0fc4628a1c54fde9a6004eb'  # Replace with your Infura project ID
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if connected
if web3.is_connected():
    print("Connected to the Polygon network")
else:
    print("Failed to connect to the Polygon network")   
    exit()

# Set up the sender's wallet details
sender_address = '0xDe2F21b06D94CCba9EF58C86f8462f78E1802b5E'  # Replace with your wallet address
private_key = '3ba3ee7a283e45fe133c7d91f462e866a70a74e05231c89792a733b23b79f6f9'  # Replace with your private key

# Set up the recipient's wallet details
recipient_address = '0x128C1DCeCd697016dD7167962aD3FFF826780b42'  # Replace with the recipient's wallet address
amount = web3.to_wei(1, 'mwei')  # Adjust according to USDT decimals (6 decimals)

# USDT contract address on Polygon
usdt_address = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'  # USDT on Polygon

# USDT ABI (only the transfer function)
usdt_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "recipient", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Create contract instance
usdt_contract = web3.eth.contract(address=usdt_address, abi=usdt_abi)

def transfer_tokens(recipient, amount):
    # Build the transaction
    transaction = usdt_contract.functions.transfer(recipient, amount).build_transaction({
        'chainId': 137,  # Polygon mainnet ID
        'gas': 200000,   # Adjust as necessary based on network conditions
        'gasPrice': web3.to_wei('1', 'gwei'),  # Adjust based on current network conditions
        'nonce': web3.eth.get_transaction_count(sender_address),
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # Wait for the transaction receipt
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

    print(f'Transaction successful with hash: {txn_hash.hex()}')
    
balance = web3.eth.get_balance(sender_address)
print(f"Balance of sender: {web3.from_wei(balance, 'ether')} MATIC")

    

# Execute the transfer
transfer_tokens(recipient_address, amount)

