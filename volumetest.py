import requests
import time
import random
import hmac
import hashlib

'''def generate_signature(secret, query_string):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
def mexc_prices(tooken_name_mex):
    url = f"https://api.mexc.com/api/v3/depth?symbol={tooken_name_mex}"
    response = requests.get(url)
    data = response.json()

    if 'bids' in data and 'asks' in data:
        mexc_price = float(data['bids'][0][0])
        mexc_selling = float(data['asks'][0][0])
        return mexc_price, mexc_selling
    else:
        raise Exception("Error fetching data")
        
        
def current():
    base_url = 'https://api.mexc.com'
    price_endpoint = '/api/v3/ticker/price'
    price_url = f"{base_url}{price_endpoint}?symbol=DEODUSDT"        
    # Fetch the current price of DEOD/USDT
    price_response = requests.get(price_url)
    if price_response.status_code != 200:
        print(f"Error fetching price: {price_response.text}")
        return None

    price_data = price_response.json()
    current_price = float(price_data['price'])
    return current_price

def mexc_prices(tooken_name_mex):
    url = f"https://api.mexc.com/api/v3/depth?symbol={tooken_name_mex}"
    response = requests.get(url)
    data = response.json()
    if 'bids' in data and 'asks' in data:
        mexc_price = float(data['bids'][0][0])
        mexc_selling = float(data['asks'][0][0])
        return mexc_price, mexc_selling, data['asks']
    else:
        raise Exception("Error fetching data")

def check_price():
    current_price = current()
    if current_price is None:
        return

    mexc_price, first_ask_price, asks = mexc_prices('DEODUSDT')
    #print(first_ask_price)

    if current_price == first_ask_price:
        next_ask_price = float(asks[1][0])
        print(f"Current price equals first ask price. Next ask price: {next_ask_price}")
        return mexc_price,next_ask_price

    else:
        print(f"Current price does not equal the first ask price.{first_ask_price}")
        return mexc_price, first_ask_price

def calculate_random_price(tooken_name_mex):
    mexc_price, mexc_selling = check_price ()
    difference = mexc_selling - mexc_price
    forty_percent_difference = difference * 0.40
    lower_bound = mexc_price
    upper_bound = mexc_price + forty_percent_difference

    random_price = None
    while random_price is None:
        price_candidate = round(random.uniform(lower_bound, upper_bound), 6)
        if price_candidate not in [round(mexc_price + 0.000001, 6), round(mexc_price + 0.000002, 6)]:
            random_price = price_candidate

    return random_price

def place_order_mexc(api_key, api_secret, size, current_price, side, tokken_name_mex):
    base_url = 'https://api.mexc.com'
    timestamp = str(int(time.time() * 1000))
    body = {
        'symbol': str(tokken_name_mex),
        'side': side,
        'type': 'LIMIT',
        'quantity': str(size),
        'price': str(current_price),
        'timestamp': timestamp
    }

    query_string = f"symbol={body['symbol']}&side={body['side']}&type={body['type']}&quantity={body['quantity']}&price={body['price']}&timestamp={body['timestamp']}"
    signature = generate_signature(api_secret, query_string)

    headers = {
        'X-MEXC-APIKEY': api_key
    }

    response = requests.post(f"{base_url}/api/v3/order?{query_string}&signature={signature}", headers=headers)
    if response.status_code == 200:
        order_info = response.json()
        print(f"Order placed on MEXC: {order_info}")
        return order_info.get('orderId')
    else:
        print(f'Error placing order on MEXC: {response.text}')
        return None

def get_order_details(api_key, api_secret, order_id, tokken_name_mex):
    base_url = 'https://api.mexc.com'
    timestamp = str(int(time.time() * 1000))
    query_string = f"symbol={tokken_name_mex}&orderId={order_id}&timestamp={timestamp}"
    signature = generate_signature(api_secret, query_string)

    headers = {
        'X-MEXC-APIKEY': api_key
    }

    response = requests.get(f"{base_url}/api/v3/order?{query_string}&signature={signature}", headers=headers)
    if response.status_code == 200:
        order_details = response.json()
        print(f"Order details retrieved: {order_details}")
        return order_details
    else:
        print(f'Error fetching order details: {response.text}')
        return None

def buy_pending_order(api_key, api_secret, order_id, tokken_name_mex):
    order_details = get_order_details(api_key, api_secret, order_id, tokken_name_mex)
    if order_details and order_details['status'] == 'NEW':  # Assuming 'NEW' means pending
        print(f"Order {order_id} is pending. Attempting to buy...")
        size = order_details['origQty']
        price = order_details['price']
        new_order_id = place_order_mexc(api_key, api_secret, size, price, 'BUY', tokken_name_mex)
        if new_order_id:
            print(f"Buy order placed successfully with order ID: {new_order_id}")
        else:
            print("Failed to place buy order.")
    else:
        print(f"Order {order_id} is not pending or could not be retrieved.")

# Example usage
api_key = "mx0vglaTf7G97pnsfC"
api_secret = "3b4d1259b9a74bf8ae9c8854ecefb2db"
current_price = calculate_random_price('DEODUSDT')
token_name_mex = 'DEODUSDT'
deod_price = 3
size = (deod_price / current_price)

# Place initial sell order
order_id = place_order_mexc(api_key, api_secret, size, current_price, 'SELL', token_name_mex)

# Buy the same order if it's pending
if order_id:
    buy_pending_order(api_key, api_secret, order_id, token_name_mex)'''
    
    
import requests
import time
import random
import hmac
import hashlib

def generate_signature(secret, query_string):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


def mexc_pricess(token_name_mex):
    #current_price=current()
    url = f"https://api.mexc.com/api/v3/depth?symbol={token_name_mex}"
    response = requests.get(url)
    data = response.json()
   # print(data)
    
    if 'bids' in data and 'asks' in data:
        mexc_buy = float(data['bids'][0][0])  # Current market price (highest bid)
        mexc_selling = float(data['asks'][0][0])
        mexc_buyquant = float(data['bids'][0][1])  # Current market price (highest bid)
        mexc_sellquant= float(data['asks'][0][1])
        print(mexc_buy,mexc_selling)
        return mexc_buy,mexc_buyquant,mexc_selling,mexc_sellquant # Current selling price (lowest ask)

    else:
        raise Exception("Error fetching data")
    
    

def mexc_prices(token_name_mex):
    #current_price=current()
    url = f"https://api.mexc.com/api/v3/depth?symbol={token_name_mex}"
    response = requests.get(url)
    data = response.json()
   # print(data)
    
    if 'bids' in data and 'asks' in data:
        mexc_buying = float(data['bids'][0][0])  # Current market price (highest bid)
        mexc_selling = float(data['asks'][0][0])
        print(mexc_buying,mexc_selling)
        return mexc_buying,mexc_selling # Current selling price (lowest ask)

    else:
        raise Exception("Error fetching data")
    
    
import random

def calculate_random_price(token_name_mex):
    mexc_price, next_ask_price = mexc_prices(token_name_mex)
    print(f'random :{mexc_price} and mexc_selling:{next_ask_price}')
    
    if mexc_price is None or next_ask_price is None:
        print("Could not retrieve prices.")
        return None
    
    difference = next_ask_price - mexc_price
    print(difference)
    
    # Calculate forty percent difference
    forty_percent_difference = difference * 0.30
    print(forty_percent_difference)
    
    # Set bounds for buying
    lower_bound_buy = mexc_price + 0.000003  # Fixed increment
    lower_bound_buy = round(lower_bound_buy, 7)
    print(f'lower bound: {lower_bound_buy}')
    
    # Adjust upper bound to be more variable
    upper_bound_buy = mexc_price + forty_percent_difference + random.uniform(0.000001, 0.000005)
    upper_bound_buy = round(upper_bound_buy, 6)
    print(f'upper bound: {upper_bound_buy}')
    # Select a random price between lower and upper bounds
    random_price = random.uniform(lower_bound_buy, upper_bound_buy)
    random_price = round(random_price, 6)  # Round the selected price to match precision
    print(f'Selected random price: {random_price}')
    
    return random_price


def place_order_mexc(api_key, api_secret, size, current_price, side, tokken_name_mex):
    base_url = 'https://api.mexc.com'
    timestamp = str(int(time.time() * 1000))
    body = {
        'symbol': str(tokken_name_mex),
        'side': side,
        'type': 'LIMIT',
        'quantity': str(size),
        'price': str(current_price),
        'timestamp': timestamp
    }

    query_string = f"symbol={body['symbol']}&side={body['side']}&type={body['type']}&quantity={body['quantity']}&price={body['price']}&timestamp={body['times>
    signature = generate_signature(api_secret, query_string)

    headers = {
        'X-MEXC-APIKEY': api_key
    }

    response = requests.post(f"{base_url}/api/v3/order?{query_string}&signature={signature}", headers=headers)
    if response.status_code == 200:
        order_info = response.json()
        print(f"Order placed on MEXC: {order_info}")
        return order_info #adding this 
    else:
        print(f'Error placing order on MEXC: {response.text}')
        return None
        


def get_open_orders(api_key, api_secret, tokken_name_mex):
    base_url = 'https://api.mexc.com'
    timestamp = str(int(time.time() * 1000))
    query_string = f"symbol={tokken_name_mex}&timestamp={timestamp}"
    signature = generate_signature(api_secret, query_string)

    headers = {
        'X-MEXC-APIKEY': api_key
    }

    response = requests.get(f"{base_url}/api/v3/openOrders?{query_string}&signature={signature}", headers=headers)
    if response.status_code == 200:
        open_orders = response.json()
        print(f"Open orders retrieved: {open_orders}")
        return open_orders
    else:
        print(f'Error fetching open orders: {response.text}')
        return []
        
def cancel_order(api_key, api_secret, order_id, tokken_name_mex):
    base_url = 'https://api.mexc.com'
    timestamp = str(int(time.time() * 1000))
    query_string = f"symbol={tokken_name_mex}&orderId={order_id}&timestamp={timestamp}"
    signature = generate_signature(api_secret, query_string)

    headers = {
        'X-MEXC-APIKEY': api_key
    }

    response = requests.delete(f"{base_url}/api/v3/order?{query_string}&signature={signature}", headers=headers)
    if response.status_code == 200:
        print(f"Order {order_id} cancelled successfully.")
        return order_id #adding this 
    else:
        print(f'Error cancelling order {order_id}: {response.text}')
        



def cancel_pending_orders(api_key, api_secret, tokken_name_mex):
    open_orders = get_open_orders(api_key, api_secret, tokken_name_mex)
    for order in open_orders:
        if order['status'] in ['NEW', 'PARTIALLY_FILLED']:  # Assuming these statuses indicate pending or partially filled
            g=cancel_order(api_key, api_secret, order['orderId'], tokken_name_mex)
            return g #adding this 
            
    def generate_random_price(lower_bound, upper_bound):
    return random.randint(lower_bound, upper_bound)

import random
import time

from flask import Flask, request, jsonify
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variable to control the trading loop
trading_active = False

# List to store logs
log_list = []

def log_message(message):
    """Helper function to log messages both to the console and the log list."""
    log_list.append(message)
    print(message)
    
def trading_loop(api_key, api_secret, tokken_name_mex):
    global trading_active
    while trading_active:
        # Fetch current prices
        mexc_buy, mexc_buyquant, mexc_sell, mexc_sellquant = mexc_pricess(token_name_mex)
        log_message(f'Current Prices - Buy: {mexc_buy}, Sell: {mexc_sell}')

        # Calculate the price difference
        diff = round(mexc_sell - mexc_buy, 7)
        log_message(f'Difference: {diff}')

        # Calculate the USDT value
        usdtb = round(mexc_buyquant * mexc_buy, 5)
        usdtc = round(mexc_sellquant * mexc_sell, 5)
        log_message(f'USDT Value - Buy: {usdtb}, Sell: {usdtc}')

        usdts = 5.5
        buy_quant = usdts / mexc_buy
        sell_quant = usdts / mexc_sell

        if diff > 0.000005:
            if random.choice([True, False]):
                deod_price = generate_random_price(10, 14)
                current_prices = calculate_random_price(token_name_mex)
                size = (deod_price / current_prices)

                sleep_time = random.uniform(1, 3)
                log_message(f"Sleeping for {sleep_time:.2f} seconds.")
                time.sleep(sleep_time)
                sell_order_id = place_order_mexc(api_key, api_secret, size, current_prices, 'SELL', token_name_mex)
                if sell_order_id:
                    log_message(f'Sell Order info: {sell_order_id}')
                    buy_order_id = place_order_mexc(api_key, api_secret, size, current_prices, 'BUY', token_name_mex)
                    if buy_order_id:
                        log_message(f'Buy Order Info: {buy_order_id}')
                    time.sleep(1)
                    d=cancel_pending_orders(api_key, api_secret, token_name_mex)
                    if d:
                       log_message(f"Order {d} cancelled successfully.")
            else:
                deod_price = generate_random_price(10, 14)
                current_prices = calculate_random_price(token_name_mex)
                size = (deod_price / current_prices)

                buy_order_id = place_order_mexc(api_key, api_secret, size, current_prices, 'BUY', token_name_mex)
                if buy_order_id:
                    log_message(f'Buy Order Info: {buy_order_id}')
                    sell_order_id = place_order_mexc(api_key, api_secret, size, current_prices, 'SELL', token_name_mex)
                    if sell_order_id:
                        log_message(f'Sell Order Info: {sell_order_id}')
                    time.sleep(1)
                    c=cancel_pending_orders(api_key, api_secret, token_name_mex)
                    if c:
                       log_message(f"Order {c} cancelled successfully.")
    
    

@app.route('/start', methods=['POST'])
def start_trading():
    global trading_active
    if not trading_active:
        trading_active = True
        api_key = request.json.get('api_key')
        api_secret = request.json.get('api_secret')
        tokken_name_mex = request.json.get('tokken_name_mex')
        trading_thread = threading.Thread(target=trading_loop, args=(api_key, api_secret, tokken_name_mex))
        trading_thread.start()
        return jsonify({"message": "Trading loop started."})
    else:
        return jsonify({"message": "Trading loop is already running."})
            
       
       
@app.route('/stop', methods=['POST'])
def stop_trading():
    global trading_active
    if trading_active:
        trading_active = False
        return jsonify({"message": "Trading stopped."}), 200
    else:
        return jsonify({"message": "Trading is not active."}), 400      
                
  
@app.route('/restart', methods=['POST'])
def restart_trading():
    global trading_active
    
    # Stop the trading loop if it's currently active
    if trading_active:
        log_message("Stopping current trading loop...")
        trading_active = False

        # Give some time for the loop to stop completely
        time.sleep(2)  # Adjust as needed for your application
    
    # Start the trading loop again
    log_message("Starting new trading loop...")
    trading_active = True
    threading.Thread(target=trading_loop, args=('your_api_key', 'your_api_secret', 'your_token')).start()
    
    return jsonify({"message": "Trading restarted."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7005, debug=True)