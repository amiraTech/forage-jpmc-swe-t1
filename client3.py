################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.


# Declaring the variables 
import json
import random
import urllib.request
import time

# Server API URLs
QUERY = "http://localhost:8080/query?id={}" 

# 500 server request
N = 500

# Stock A and Stock B - this defines 2 empty lists and store data for 2 correlated stocks
stockA_data = []
stockB_data = []

# This stores the stock information
stock_info = []



def getDataPoint(quote):
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2 # Calculate the average number
    return stock, bid_price, ask_price, price


def getRatio(price_a, price_b):
    if price_b == 0:
        return 0
    return price_a / price_b


# Main
if __name__ == "__main__":
    while True:
        quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())

        # Iterate through the quotes and collect data for two correlated stocks (e.g., Stock A and Stock B)
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)

           # Check if the stock is in the dictionary
            if stock not in stock_info:
                stock_info[stock] = {
                    'bid_prices' :[],
                    'ask_prices' :[],
                    'prices' :[],
                    'ratios' :[],
                }

            stock_info[stock]['bid_prices'].append(bid_price)
            stock_info[stock]['ask_prices'].append(ask_price)
            stock_info[stock]['prices'].append(price)
  
            # Decides which stock is Stock A and which is Stock B
            if stock == 'STOCK_A':
                stockA_data.append(price)
            elif stock == 'STOCK_B':
                stockB_data.append(price)

        # Calculate the ratio 
        if len(stockA_data) > 0 and len(stockB_data) > 0:
            last_price_A = stockA_data[-1]
            last_price_B = stockB_data[-1]
            ratio = getRatio(last_price_A, last_price_B)
            stock_info[stock]['ratios'].append(ratio)

            # Print the ratio and any other relevant information
            print(f"Ratio: {ratio}")
            print(f"Stock: {stock}")
            print(f"Bid Price: {bid_price}")
            print(f"Ask Price: {ask_price}")
            print(f"Price: {price}")
            print(f"Ratio: {ratio}")
        
        # Sleep for a while before making the next request (adjust the sleep time as needed)
        time.sleep(10)  

        # Print the stock information
        print("Stock Information")
        print(stock_info)
