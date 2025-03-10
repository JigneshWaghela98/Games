import yfinance as yf
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Function to fetch data and save to CSV
def fetch_and_save_data(ticker, start_date, end_date, save_path):
    # Fetch historical data
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        raise ValueError("No data found for the given ticker symbol.")
    
    # Save the historical data to CSV
    csv_file_path = os.path.join(save_path, f'{ticker}.csv')
    data.to_csv(csv_file_path)

    print(f"Historical data saved to {csv_file_path}")

    return data

# Function to apply EMA strategy
def apply_ema_strategy(data):
    short_window = 50  # Fixed short EMA period
    long_window = 200  # Fixed long EMA period
    
    # Calculate EMAs
    data['Short_EMA'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['Long_EMA'] = data['Close'].ewm(span=long_window, adjust=False).mean()

    # Generate signals
    data['Signal'] = 0  # Default to no position
    data['Signal'][short_window:] = np.where(data['Short_EMA'][short_window:] > data['Long_EMA'][short_window:], 1, 0)
    data['Position'] = data['Signal'].diff()  # Buy (1) or Sell (-1)

    return data

# Function to plot prices and EMAs with buy/sell signals
def plot_price_and_ema(data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.5)
    plt.plot(data.index, data['Short_EMA'], label='50-day EMA', color='red', alpha=0.75)
    plt.plot(data.index, data['Long_EMA'], label='200-day EMA', color='green', alpha=0.75)

    buy_signals = data[data['Position'] == 1]
    sell_signals = data[data['Position'] == -1]

    # Plot buy signals
    plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy Signal', s=100)
    # Plot sell signals
    plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', label='Sell Signal', s=100)

    plt.title(f'Price and EMA Strategy Signals for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

# Main function to run the trading bot
def run_trading_bot():
    ticker_input = input("Enter the ticker symbol (e.g., AAPL or EURUSD=X): ")
    start_date_input = input("Enter the start date (YYYY-MM-DD): ")
    end_date_input = input("Enter the end date (YYYY-MM-DD): ")
    save_path_input = input("Enter the directory where you want to save the CSV file: ")

    # Ensure the directory exists
    if not os.path.exists(save_path_input):
        os.makedirs(save_path_input)

    # Fetch data
    historical_data = fetch_and_save_data(ticker_input, start_date_input, end_date_input, save_path_input)

    # Apply EMA strategy
    ema_data = apply_ema_strategy(historical_data)

    # Display buy and sell signals
    buy_signals = ema_data[ema_data['Position'] == 1]
    sell_signals = ema_data[ema_data['Position'] == -1]

    print("\nBuy Signals:")
    print(buy_signals[['Close', 'Short_EMA', 'Long_EMA', 'Position']])

    print("\nSell Signals:")
    print(sell_signals[['Close', 'Short_EMA', 'Long_EMA', 'Position']])

    # Save the EMA signals to a new CSV file
    ema_csv_file_path = os.path.join(save_path_input, f'{ticker_input}_ema_signals.csv')
    ema_data.to_csv(ema_csv_file_path)
    print(f"EMA signals saved to {ema_csv_file_path}")

    # Plot prices and EMAs
    plot_price_and_ema(ema_data, ticker_input)

# Run the trading bot
if __name__ == "__main__":
    run_trading_bot()

#Arbitrage 
#Portfolio management  
#Predictive             