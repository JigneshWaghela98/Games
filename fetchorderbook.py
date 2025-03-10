import hmac
import hashlib
import requests
import time

API_KEY = '89db284cbefc2fba25d7460b8e1e2ed70cfd8573'
API_SECRET = '6255080761902819625754b6b634a92e8c9c3b9aedab7e51c1bc301c583cb90d'
API_MEMO = 'vbot'

def fetch_order_book(symbol):
    url = f"https://api-cloud.bitmart.com/spot/quotation/v3/books?symbol={symbol}"
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    query_string = f"symbol={symbol}" 
    payload = ""

    sign = hmac.new(
        API_SECRET.encode('utf-8'),
        (timestamp + '#' + API_MEMO + '#' + method + '#' + query_string + '#' + payload).encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    headers = {
        'X-BM-KEY': API_KEY,
        'X-BM-SIGN': sign,
        'X-BM-TIMESTAMP': timestamp,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['code'] == 1000:
            return data['data']
        else:
            print(f"Error fetching order book: {data['message']}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

def get_signature(secret_key, params):
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def get_open_orders(symbol):
    url = 'https://api-cloud.bitmart.com/spot/v1/orders'
    timestamp = str(int(time.time() * 1000))
    params = {
        'symbol': symbol,
        'status': '4',  # Partially Filled and Canceling
        'offset': 1,
        'limit': 50,
        'timestamp': timestamp
    }
    signature = get_signature(API_SECRET, params)
    headers = {
        'X-BM-KEY': API_KEY,
        'X-BM-SIGN': signature,
        'X-BM-TIMESTAMP': timestamp,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def check_order_matches(order_book, open_orders):
    asks = order_book['asks']
    bids = order_book['bids']

    results = []

    for order in open_orders['data']['orders']:
        order_price = float(order['price'])
        order_size = order['size']

        for ask in asks:
            ask_price = float(ask[0])
            size = ask[1]
            match = '*' if ask_price == order_price else ''
            results.append({'price': ask_price, 'size': size, 'type': 'ask', 'match': match})

        for bid in bids:
            bid_price = float(bid[0])
            size = bid[1]
            match = '*' if bid_price == order_price else ''
            results.append({'price': bid_price, 'size': size, 'type': 'bid', 'match': match})

    return results

def print_vertical_table(data, title):
    print(f"\n{title}")
    print("=" * len(title))
    for key, value in data.items():
        print(f"{key}: {value}")
    print()

# Example usage
symbol = 'DEOD_USDT'
j = fetch_order_book(symbol)
k = get_open_orders(symbol)

if j and k:
    print_vertical_table(j, "Order Book Data")
    print_vertical_table(k['data'], "Open Orders Data")

    matches = check_order_matches(j, k)
    print("\nMatches:")
    print("=" * 7)
    for match in matches:
        print(f"Price: {match['price']}, Size: {match['size']}, Type: {match['type']}, Match: {match['match']}")
