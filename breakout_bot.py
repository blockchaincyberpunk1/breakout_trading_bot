import os
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv

# Load API keys from the .env file
load_dotenv()
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")  # Load Alpaca API Key from environment
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")  # Load Alpaca Secret Key from environment
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")  # Load Alpha Vantage API Key from environment

# Initialize Alpaca API
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url="https://paper-api.alpaca.markets")
# Initialize the Alpaca API client for trading. The 'paper-api' URL is used for paper trading.

# Define your trading strategy here
def breakout_strategy(data):
    # Implement your breakout strategy using data
    # Example: Buy when the price breaks above the 20-day high

    # Calculate the 20-day high by rolling maximum of the 'close' prices
    data['20-day_high'] = data['close'].rolling(window=20).max()

    # Create a 'position' column based on the breakout condition
    data['position'] = np.where(data['close'] > data['20-day_high'], 1, 0)
    return data

# Fetch historical data from Alpha Vantage
def fetch_alpha_vantage_data(symbol, outputsize='full'):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    # Create an Alpha Vantage TimeSeries instance with your API key
    data, meta_data = ts.get_daily(symbol=symbol, outputsize=outputsize)
    # Fetch daily historical data for the specified symbol
    
    return data

# Main function
def main():
    symbol = "AAPL"  # Change to your desired symbol
    outputsize = 'full'  # Adjust to 'compact' if you need less historical data
    
    # Fetch historical data using Alpha Vantage
    data = fetch_alpha_vantage_data(symbol, outputsize)
    
    # Process data and apply the trading strategy
    data = breakout_strategy(data)
    
    # Perform trading based on your strategy
    for index, row in data.iterrows():
        if row['position'] == 1:
            # Buy logic (e.g., place an order using Alpaca API)
            api.submit_order(
                symbol=symbol,
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            # Log the trade in a file
            with open('logs/trading_log.txt', 'a') as log_file:
                log_file.write(f"Bought {symbol} at {row['close']}\n")

if __name__ == "__main__":
    main()



""" 
Explanation:

Start by importing the necessary libraries and modules for our trading bot.

The .env file is loaded using load_dotenv(), which stores API keys securely as environment variables.

The Alpaca API is initialized with the provided API keys. Use the paper trading URL here (base_url="https://paper-api.alpaca.markets") for testing without real money.

breakout_strategy is a function that implements the trading strategy. In this example, it calculates the 20-day high and determines the trading position based on the breakout condition.

fetch_alpha_vantage_data is a function to fetch historical data from Alpha Vantage for a specified symbol and output size (default is 'full').

In the main function, we specify the trading symbol (e.g., "AAPL") and the output size.

Fetch historical data using Alpha Vantage and apply the breakout strategy to it.

If the breakout strategy indicates a position should be taken (position == 1), simulate a buy order using Alpaca's API for paper trading. This order is logged in a file.

Finally, run the main function when the script is executed.

"""