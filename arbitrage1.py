import websocket
import json
import threading
import time
from queue import Queue

# Global queues for sharing prices between threads
bitmart_queue = Queue()
mexc_queue = Queue()

# Initialize variables to store the latest prices
bitmart_price = None
mexc_price = None

def on_message_bitmart(ws, message):
    global bitmart_price
    data = json.loads(message)
    if 'table' in data and data['table'] == 'spot/ticker':
        for ticker in data['data']:
            if ticker['symbol'] == 'DEOD_USDT':
                bitmart_price = float(ticker['last_price'])
                size = ticker['bid_sz']
                sell_price = ticker['ask_px']
                ask_sz = ticker['ask_sz']
                
                # Put the data in the queue
                bitmart_queue.put({
                    "price": bitmart_price,
                    "size": size,
                    "sell_price": sell_price,
                    "ask_sz": ask_sz
                })
                
                print(f"BitMart DEOD/USDT Price: {bitmart_price}, Size: {size}")
                print(f"BitMart Selling Price: {sell_price}, Selling quantity: {ask_sz}")

def on_message_mexc(ws, message):
    global mexc_price
    data = json.loads(message)
    if 'd' in data:
        ticker_data = data['d']
        
        ask_price = float(ticker_data['a'])
        mexc_price = ask_price
        ask_quantity = ticker_data['A']
        bid_price = float(ticker_data['b'])
        bid_quantity = ticker_data['B']
        
        # Put the data in the queue
        mexc_queue.put({
            "ask_price": ask_price,
            "ask_quantity": ask_quantity,
            "bid_price": bid_price,
            "bid_quantity": bid_quantity
        })
        
        print(f"Mexc DEOD/USDT current Bid Price: {bid_price}, current Bid Quantity: {bid_quantity}")
        print(f"Mexc DEOD/USDT selling Ask Price: {ask_price}, selling Ask Quantity: {ask_quantity}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open_bitmart(ws):
    subscribe_message = {
        "op": "subscribe",
        "args": ["spot/ticker:DEOD_USDT"]
    }
    ws.send(json.dumps(subscribe_message))

def on_open_mexc(ws):
    message = {
        "method": "SUBSCRIPTION",
        "params": ["spot@public.bookTicker.v3.api@DEODUSDT"]
    }
    ws.send(json.dumps(message))

def run_websocket(url, on_open, on_message):
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(ping_interval=5, ping_timeout=4)

#Function for buying from either of exchange at low price
def compare_prices_and_buy():
    global bitmart_price, mexc_price
    if bitmart_price is not None and mexc_price is not None: 
        if bitmart_price < mexc_price:
            print(f"Buying from BitMart at {bitmart_price}")
            buy_from_exchange('BitMart', bitmart_price)
        elif mexc_price < bitmart_price:
            print(f"Buying from MEXC at {mexc_price}")
            buy_from_exchange('MEXC', mexc_price)
        else:
            print("Prices are equal, no action taken.")

def buy_from_exchange(exchange_name, price):
    # This is a placeholder function. Implement actual buying logic or API calls here.
    print(f"Placing order on {exchange_name} at price {price}")

def main():
    # Define WebSocket URLs
    bitmart_url = "wss://ws-manager-compress.bitmart.com/api?protocol=1.1"
    mexc_url = "wss://wbs.mexc.com/ws"
    
    # Start WebSocket connections
    bitmart_thread = threading.Thread(target=run_websocket, args=(bitmart_url, on_open_bitmart, on_message_bitmart))
    mexc_thread = threading.Thread(target=run_websocket, args=(mexc_url, on_open_mexc, on_message_mexc))
    
    bitmart_thread.start()
    mexc_thread.start()
    
    while True:
        # Process BitMart queue
        if not bitmart_queue.empty():
            bitmart_data = bitmart_queue.get()
            print("Received BitMart Data:", bitmart_data)
    
        # Process MEXC queue
        if not mexc_queue.empty():
            mexc_data = mexc_queue.get()
            print("Received MEXC Data:", mexc_data)
        
        # Compare prices and decide where to buy
        compare_prices_and_buy()
        
        # Sleep to prevent high CPU usage
        time.sleep(1)

if __name__ == "__main__":
    main()
