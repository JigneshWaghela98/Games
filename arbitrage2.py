import requests
import time
import hmac
import hashlib
import json
import websocket
import threading

# Replace with your own API keys and secrets
bitmart_api_key = '9935ff7064f62790aa225c8d6e390df381e3ef6b'
bitmart_api_secret = '37b4458fcbdc3f5d20d6bd75b30ce6b89fbfe79c9972b166e5e4265450c6dc32'
bitmart_memo = 'rbot'
mexc_api_key = 'mx0vglD2hg4NpEtIuE'
mexc_api_secret = 'f7b4796e681347f3b7ce4846fc87d64c'

# Global variables for prices
bitmart_price = 0.0
bitmart_selling = 0.0
mexc_price = 0.0
mexc_selling = 0.0

# Common utility functions
def get_timestamp():
    return str(int(time.time() * 1000))

def generate_signature(api_secret, message):
    return hmac.new(api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

# Fetch balances
def fetch_balance(api_key, api_secret, url, is_bitmart=True, memo=''):
    timestamp = get_timestamp()
    headers = {'X-BM-KEY': api_key, 'X-BM-TIMESTAMP': timestamp, 'Content-Type': 'application/json'}
    
    if is_bitmart:
        sign = generate_signature(api_secret, f"{timestamp}#{memo}#GET###")
        headers['X-BM-SIGN'] = sign
        response = requests.get(url, headers=headers)
    else:
        query_string = f"timestamp={timestamp}"
        sign = generate_signature(api_secret, query_string)
        response = requests.get(f"{url}?{query_string}&signature={sign}", headers={'X-MEXC-APIKEY': api_key})
    
    data = response.json()
    return data

def fetch_bitmart_balance():
    data = fetch_balance(bitmart_api_key, bitmart_api_secret, "https://api-cloud.bitmart.com/account/v1/wallet", memo=bitmart_memo)
    wallet = data['data']['wallet'] if data['code'] == 1000 else []
    balances = {c['currency']: {'available': float(c['available']), 'total': float(c['available']) + float(c['frozen'])} for c in wallet if c['currency'] in ['DEOD', 'USDT']}
    return balances.get('USDT', {}).get('total', 0), balances.get('DEOD', {}).get('total', 0)

def fetch_mexc_balance():
    data = fetch_balance(mexc_api_key, mexc_api_secret, "https://api.mexc.com/api/v3/account", is_bitmart=False)
    balances = {b['asset']: b['free'] for b in data.get('balances', []) if b['asset'] in ['DEOD', 'USDT']}
    return float(balances.get('USDT', 0)), float(balances.get('DEOD', 0))

# Place orders
def place_order(api_key, api_secret, side, size, price, is_bitmart=True):
    url = ('https://api-cloud.bitmart.com/spot/v2/submit_order' if is_bitmart else 'https://api.mexc.com/api/v3/order')
    body = json.dumps({'symbol': 'DEOD_USDT', 'side': side, 'type': 'LIMIT', 'quantity': str(size), 'price': str(price)})
    
    if is_bitmart:
        timestamp = get_timestamp()
        signature = generate_signature(api_secret, f"{timestamp}#{bitmart_memo}#{body}")
        headers = {'Content-Type': 'application/json', 'X-BM-KEY': api_key, 'X-BM-TIMESTAMP': timestamp, 'X-BM-SIGN': signature}
    else:
        query_string = f"symbol=DEODUSDT&side={side}&type=LIMIT&quantity={size}&price={price}&timestamp={get_timestamp()}"
        signature = generate_signature(api_secret, query_string)
        headers = {'X-MEXC-APIKEY': api_key}
        url += f"?{query_string}&signature={signature}"
    
    response = requests.post(url, headers=headers, json={} if is_bitmart else None)
    print(f"Order placed on {'BitMart' if is_bitmart else 'MEXC'}: {response.json()}")

# WebSocket functions
def on_message(ws, message, is_bitmart=True):
    global bitmart_price, bitmart_selling, mexc_price, mexc_selling
    data = json.loads(message)
    if is_bitmart and 'table' in data and data['table'] == 'spot/ticker':
        for ticker in data['data']:
            if ticker['symbol'] == 'DEOD_USDT':
                bitmart_price = float(ticker['bid_px'])
                bitmart_selling = float(ticker['ask_px'])
    elif not is_bitmart and 'd' in data:
        ticker_data = data['d']
        if 'a' in ticker_data:
            mexc_price = float(ticker_data['b'])
            mexc_selling = float(ticker_data['a'])

def fetch_price(is_bitmart=True):
    url = "wss://ws-manager-compress.bitmart.com/api?protocol=1.1" if is_bitmart else "wss://wbs.mexc.com/ws"
    ws = websocket.WebSocketApp(url, on_message=lambda ws, msg: on_message(ws, msg, is_bitmart))
    ws.run_forever(ping_interval=5, ping_timeout=4)

# Arbitrage strategy
def check_arbitrage(profit_threshold, transaction_fee, desired_price):
    while True:
        bitmart_usdt, bitmart_deod = fetch_bitmart_balance()
        mexc_usdt, mexc_deod = fetch_mexc_balance()
        if bitmart_price and mexc_price:
            if bitmart_selling < mexc_price:
                amount = desired_price / bitmart_selling
                if ((mexc_price - bitmart_selling) / mexc_price * 100 - transaction_fee) >= profit_threshold:
                    place_order(bitmart_api_key, bitmart_api_secret, 'buy', amount, bitmart_selling)
                    place_order(mexc_api_key, mexc_api_secret, 'SELL', amount, mexc_price, is_bitmart=False)
            elif mexc_selling < bitmart_price:
                amount = desired_price / mexc_selling
                if ((bitmart_price - mexc_selling) / bitmart_price * 100 - transaction_fee) >= profit_threshold:
                    place_order(mexc_api_key, mexc_api_secret, 'BUY', amount, mexc_selling, is_bitmart=False)
                    place_order(bitmart_api_key, bitmart_api_secret, 'sell', amount, bitmart_price)

        time.sleep(5)

# Start threads for WebSocket connections
threading.Thread(target=fetch_price, args=(True,)).start()
threading.Thread(target=fetch_price, args=(False,)).start()

# Start arbitrage check
check_arbitrage(0.15, 0.004, 6.0)
