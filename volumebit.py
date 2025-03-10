from flask import Flask, request, jsonify
import threading
import time
import random
import requests
import hmac
import hashlib
import json
import logging

app = Flask(__name__)

# Set up logging for console output
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Global variables to control the trading loop
trading_active = False
trading_thread = None
logs = []

def get_timestamp():
    return str(int(time.time() * 1000))


def generate_signature(api_secret, query_string):
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def bitmart_prices():
    url = f"https://api-cloud.bitmart.com/spot/v1/symbols/book?symbol=DEOD_USDT"
    response = requests.get(url)
    data = response.json()
    #print(data)

    if data['code'] == 1000:
        bitmart_price = data['data']['buys'][0]['price']
        bitmart_selling = data['data']['sells'][0]['price']
        return bitmart_price,bitmart_selling 
    else:
        raise Exception(f"Error fetching data: {data['message']}")

def bitmart_pricess():
    url = f"https://api-cloud.bitmart.com/spot/v1/symbols/book?symbol=DEOD_USDT"
    response = requests.get(url)
    data = response.json()
    #print(data)

    if data['code'] == 1000:
        bit_price = data['data']['buys'][0]['price']
        bit_buyquant = data['data']['buys'][0]['amount']
        bit_selling = data['data']['sells'][0]['price']
        bit_sellquant = data['data']['sells'][0]['amount']
        return bit_price,bit_buyquant,bit_selling,bit_sellquant 
    else:
        raise Exception(f"Error fetching data: {data['message']}")    

# Function to manage logs
def add_log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    logs.append(f"{timestamp}: {message}")

    # Clear logs older than 1 hour
    while len(logs) > 0 and (time.time() - time.mktime(time.strptime(logs[0].split(": ")[0], "%Y-%m-%d %H:%M:%S"))) > 3600:
        logs.pop(0)

# Trading loop function
'''def trading_loop(api_key, api_secret, api_memo, token_name_bit, sellpricef, sellpricet, buypricef, buypricet, timef, timet):
    global trading_active
    while trading_active:
        try:
            # Ensure all required functions are defined
            if 'bitmart_pricess' not in globals() or 'generate_random_price' not in globals() or \
               'calculate_random_price' not in globals() or 'place_order_bit' not in globals() or \
               'cancel_pending_orders' not in globals():
                raise NotImplementedError("Required functions are not implemented.")

            # Fetch current prices
            mexc_buy, mexc_buyquant, mexc_sell, mexc_sellquant = bitmart_pricess()

            # Calculate the price difference
            diff = round(mexc_sell - mexc_buy, 7)
            add_log(f'Difference: {diff}')

            # Calculate the USDT value
            usdtb = round(mexc_buyquant * mexc_buy, 5)
            usdtc = round(mexc_sellquant * mexc_sell, 5)
            add_log(f'USDT Value: {usdtb}')

            usdts = 5.5
            buy_quant = usdts / mexc_buy
            sell_quant = usdts / mexc_sell

            if diff > 0.000005:
                if random.choice([True, False]):
                    deod_price = generate_random_price(sellpricef, sellpricet)
                    current_prices = calculate_random_price()
                    size = deod_price / current_prices
                    place_order_bit(api_key, api_secret, api_memo, size, current_prices, 'sell', token_name_bit)
                    place_order_bit(api_key, api_secret, api_memo, size, current_prices, 'buy', token_name_bit)
                else:
                    deod_price = generate_random_price(buypricef, buypricet)
                    current_prices = calculate_random_price()
                    size = deod_price / current_prices
                    place_order_bit(api_key, api_secret, api_memo, size, current_prices, 'buy', token_name_bit)
                    place_order_bit(api_key, api_secret, api_memo, size, current_prices, 'sell', token_name_bit)

                time.sleep(4)
                cancel_pending_orders(api_key, api_secret, api_memo, token_name_bit)

            sleep_time = random.uniform(timef, timet)
            add_log(f"Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
        except Exception as e:
            add_log(f"Error: {e}")'''
def generate_random_price(lower_bound, upper_bound):
    return random.randint(lower_bound, upper_bound)
def calculate_random_price():
    mexc_price, next_ask_price = bitmart_prices()
    print(f'random :{mexc_price} and mexc_selling:{next_ask_price}')
    mexc_price=float(mexc_price)
    next_ask_price=float(next_ask_price)
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
    return random_price

def generate_random_price(lower_bound, upper_bound):
    return random.randint(lower_bound, upper_bound)

def place_order_bit(bitmart_api_key, api_secret,api_memo,size,current_price,side,tokken_name_bit):
    base_url = 'https://api-cloud.bitmart.com'
    endpoint = '/spot/v2/submit_order'
    url = base_url + endpoint

    '''# Fetch the current price of DEOD/USDT
    price_endpoint = '/spot/v1/ticker'
    price_url = f"{base_url}{price_endpoint}?symbol=DEOD_USDT"
    price_response = requests.get(price_url)
    
    if price_response.status_code != 200:
        print(f"Error fetching price: {price_response.text}")
        return

    price_data = price_response.json()
    current_price = float(price_data['data']['tickers'][0]['last_price'])'''

    # Calculate the size of DEOD to buy with the available USDT balance
    #size = usdt_balance / current_price
    if size <= 0:
        print("Insufficient balance to buy DEOD bitmart.")
        return "Insufficient balance to buy DEOD bitmart."

    timestamp = str(int(time.time() * 1000))
    body = {
        'size': str(size),  # Order size
        'price': str(current_price),  # Order price
        'side': side,  # 'buy' or 'sell'
        'symbol': str(tokken_name_bit),#'DEOD_USDT',  # Trading pair
        'type': 'limit'  # Order type: 'limit' or 'market'
    }
    body_json = json.dumps(body)
    message = f"{timestamp}#{api_memo}#{body_json}"
    signature = generate_signature(api_secret, message)

    headers = {
        'Content-Type': 'application/json',
        'X-BM-KEY': bitmart_api_key,
        'X-BM-TIMESTAMP': timestamp,
        'X-BM-SIGN': signature
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        print(f"Order placed on BitMart: {response.json()}")
    else:
        print(f'Error placing order on BitMart: {response.text}')
        print(f'Generated Signature: {signature}')
        print(f'Timestamp: {timestamp}')
        print(f'Body: {body_json}')


def cancel_pending_orders(api_key, api_secret, api_memo, token_name_bit):
    base_url = 'https://api-cloud-v2.bitmart.com'
    endpoint = '/spot/v4/cancel_all'
    url = base_url + endpoint

    timestamp = str(int(time.time() * 1000))
    body = {
        'symbol': str(token_name_bit)  # Trading pair
    }
    body_json = json.dumps(body)
    message = f"{timestamp}#{api_memo}#{body_json}"
    signature = generate_signature(api_secret, message)

    headers = {
        'Content-Type': 'application/json',
        'X-BM-KEY': api_key,
        'X-BM-TIMESTAMP': timestamp,
        'X-BM-SIGN': signature
    }
    return "order cancel succesful"



            
    # Trading loop function with enhanced logging
def trading_loop(api_key, api_secret, api_memo, token_name_bit, sellpricef, sellpricet, buypricef, buypricet, timef, timet):
    global trading_active
    while trading_active:
        try:
            add_log("Trading loop started.")
            
            # Ensure all required functions are defined
            required_functions = [
                'bitmart_pricess', 'generate_random_price', 
                'calculate_random_price', 'place_order_bit', 
                'cancel_pending_orders'
            ]
            for func in required_functions:
                if func not in globals():
                    raise NotImplementedError(f"Required function '{func}' is not implemented.")

            # Fetch current prices
            mexc_buy, mexc_buyquant, mexc_sell, mexc_sellquant = bitmart_pricess()
            add_log(f"Fetched prices - Buy: {mexc_buy}, Buy Quant: {mexc_buyquant}, Sell: {mexc_sell}, Sell Quant: {mexc_sellquant}")

            # Calculate the price difference
            diff = round(float(mexc_sell - mexc_buy, 7))
            add_log(f"Price Difference: {diff}")

            # Calculate the USDT value
            usdtb = round(float(mexc_buyquant * mexc_buy, 5))
            usdtc = round(float(mexc_sellquant * mexc_sell, 5))
            add_log(f"USDT Value - Buy: {usdtb}, Sell: {usdtc}")

            usdts = 5.5
            buy_quant = usdts / mexc_buy
            sell_quant = usdts / mexc_sell
            add_log(f"Calculated Quantities - Buy: {buy_quant}, Sell: {sell_quant}")

            if diff > 0.000005:
                action = random.choice(["sell", "buy"])
                deod_price = generate_random_price(sellpricef, sellpricet) if action == "sell" else generate_random_price(buypricef, buypricet)
                current_prices = calculate_random_price()
                size = deod_price / current_prices
                add_log(f"Placing orders - Action: {action}, Size: {size}, Current Prices: {current_prices}")

                place_order_bit(api_key, api_secret, api_memo, size, current_prices, action, token_name_bit)
                place_order_bit(api_key, api_secret, api_memo, size, current_prices, "buy" if action == "sell" else "sell", token_name_bit)

                time.sleep(4)
                cancel_pending_orders(api_key, api_secret, api_memo, token_name_bit)
                add_log(f"Orders placed and pending orders cancelled for token: {token_name_bit}")

            sleep_time = random.uniform(timef, timet)
            add_log(f"Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
        except Exception as e:
            add_log(f"Error in trading loop: {e}")
            import traceback
            traceback_log = traceback.format_exc()
            add_log(f"Error Traceback: {traceback_log}")
        

@app.route('/start', methods=['POST'])
def start_trading():
    global trading_active, trading_thread
    if trading_active:
        return jsonify({"message": "Trading is already active."}), 400

    data = request.json
    trading_active = True
    trading_thread = threading.Thread(target=trading_loop, args=(
        data['api_key'], data['api_secret'], data['api_memo'],
        data['token_name_bit'], data['sellpricef'], data['sellpricet'],
        data['buypricef'], data['buypricet'], data['timef'], data['timet']
    ))
    trading_thread.start()
    add_log("Trading started.")
    return jsonify({"message": "Trading started."})

@app.route('/stop', methods=['POST'])
def stop_trading():
    global trading_active, trading_thread
    if not trading_active:
        return jsonify({"message": "Trading is not active."}), 400

    trading_active = False
    if trading_thread:
        trading_thread.join()
    add_log("Trading stopped.")
    return jsonify({"message": "Trading stopped."})

@app.route('/restart', methods=['POST'])
def restart_trading():
    stop_response = stop_trading()
    if stop_response.status_code == 400:
        return stop_response

    start_response = start_trading()
    return start_response

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({"logs": logs})

if __name__ == '__main__':
    try:
        app.run(debug=True, port=7000)
    except Exception as e:
        print(f"Failed to start the app: {e}")
