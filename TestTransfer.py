from web3 import Web3
from flask import Flask, request, jsonify

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
usdt_amount = web3.to_wei(1, 'mwei')  # Adjust according to USDT decimals (6 decimals)

# USDT contract address on Polygon
#usdt_address = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'  # USDT on Polygon
usdt_address = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'
# Complete USDT ABI (including balanceOf)
usdt_abi = [
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
         "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "recipient", "type": "address"}, {"name": "amount", "type": "uint256"}],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Create contract instance
usdt_contract = web3.eth.contract(address=usdt_address, abi=usdt_abi)

def get_usdt_balance(address):
    balance = usdt_contract.functions.balanceOf(address).call()
    return balance

# Check USDT balance before executing transfer
usdt_balance = get_usdt_balance(sender_address)
print(f"Raw USDT Balance of sender (in Wei): {usdt_balance}")
# Convert balance to USDT
usdt_balance_in_usdt = usdt_balance / 10**6  # Divide by 1,000,000 to convert to USDT
print(f"USDT Balance of sender: {usdt_balance_in_usdt} USDT")

 
# Display MATIC balance
matic_balance = web3.eth.getbalance(sender_address)
print(f"MATIC Balance of sender: {web3.from_wei(matic_balance, 'ether')} MATIC")

# Execute USDT transfer if balance is sufficient
if usdt_balance < usdt_amount:
    print("Insufficient USDT balance to complete the transfer.")
else:
    # Build the transaction for USDT transfer
    transaction = usdt_contract.functions.transfer(recipient_address, usdt_amount).build_transaction({
    'chainId': 137,  # Polygon mainnet ID
    'gas': 200000,   # Adjust as necessary based on network conditions
    'gasPrice': web3.eth.gas_price,  # Use the current gas price
    'nonce': web3.eth.get_transaction_count(sender_address),
})

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

# Print the signed transaction for debugging
print(signed_txn)

# Send the transaction
try:
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)  # Corrected here
    print(f'USDT Transaction sent! Hash: {txn_hash.hex()}')

    # Wait for the transaction receipt
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    print(f'USDT Transaction successful with hash: {txn_hash.hex()}')

except Exception as e:
    print(f'Error sending USDT transaction: {e}')


