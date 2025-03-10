from flask import Flask, request, jsonify
from web3 import Web3
import requests

app = Flask(__name__)

# Connect to Polygon network via Infura
infura_url = 'https://polygon-mainnet.infura.io/v3/79467c63c0fc4628a1c54fde9a6004eb'
web3 = Web3(Web3.HTTPProvider(infura_url))

# USDT contract address on Polygon
usdt_address = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'
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

def get_gas_price_in_gwei():
    try:
        response = requests.get('https://ethgasstation.info/api/ethgasAPI.json')
        response.raise_for_status()  # Raise an error for bad status codes
        gas_data = response.json()
        
        # Return the fast gas price in Gwei
        return gas_data['fast'] / 10  # Convert from gwei/10 to gwei
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}. Response content: {response.text}")
    return None  # Return None or a default value if there's an error

def get_eth_price_in_usdt():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        response.raise_for_status()
        eth_data = response.json()
        return eth_data['ethereum']['usd']
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
        return None

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    sender_address = data.get('sender_address')
    private_key = data.get('private_key')
    recipient_address = data.get('recipient_address')
    usdt_amount = web3.to_wei(data.get('amount', 0), 'mwei')  # USDT amount
    gas_price_usdt = data.get('gas_price_usdt', 0)  # Gas price in USDT

    # Get current gas price in Gwei
    gas_price_gwei = get_gas_price_in_gwei()
    if gas_price_gwei is None:
        return jsonify({"error": "Failed to fetch gas price."}), 500

    # Get current ETH price in USDT
    eth_price_usdt = get_eth_price_in_usdt()
    if eth_price_usdt is None:
        return jsonify({"error": "Failed to fetch ETH price."}), 500

    # Convert gas price from USDT to Gwei
    gas_price_gwei_from_usdt = (gas_price_usdt * 1e-6) / (eth_price_usdt / 1e9)  # Convert USDT to Gwei

    # Check USDT balance
    usdt_balance = usdt_contract.functions.balanceOf(sender_address).call()
    if usdt_balance < usdt_amount:
        return jsonify({"error": "Insufficient USDT balance to complete the transfer."}), 400

    # Build the transaction for USDT transfer
    transaction = usdt_contract.functions.transfer(recipient_address, usdt_amount).build_transaction({
        'chainId': 137,
        'gas': 200000,
        'gasPrice': web3.to_wei(gas_price_gwei_from_usdt, 'gwei'),  # Use converted gas price
        'nonce': web3.eth.get_transaction_count(sender_address),
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    try:
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        
        # Add conversion information to the response
        return jsonify({
            "transaction_hash": txn_hash.hex(),
            "status": "success",
            "usdt_amount": data.get('amount', 0),
            "gas_price_usdt": gas_price_usdt,
            "converted_gwei": gas_price_gwei_from_usdt
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
