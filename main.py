import os
from dotenv import load_dotenv
import pandas as pd
import openpyxl

from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient

from SimpleMovingAverage import SimpleMovingAverage
from BollingerBands import BollingerBand

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

trading_client = StockHistoricalDataClient(api_key, api_secret)

request_params = StockBarsRequest(
    symbol_or_symbols=["GE"],
    timeframe=TimeFrame.Day,
    start="2019-01-01 00:00:00",
    end="2021-12-30 00:00:00"
)

bars = trading_client.get_stock_bars(request_params)
bars_df = bars.df
close_df = bars_df['close']

ma = SimpleMovingAverage(20)

def calculate_bollinger_profit(holdings, closing_data):
    collection = {
        "date" : [],
        "closing_price" : [],
        "simple_moving_average" : [],
        "upper_band" : [],
        "lower_band" : [],
        "buy" : [],
        "sell" : [],
        "percent_change" : []
    }

    #amount_current will be what stores the new profits/losses, which will start at whatever the holdings are
    amount_current = holdings
    #added will take into account how much money is being added after sale of shares
    added = 0
    #number of shares purchased
    shares_owned = 0
    #total value of shares bought
    asset_value = 0
    #bool that takes into account if any shares are owned
    has_share = False

    for index in range(len(closing_data)):
        to_buy = False
        to_sell = False
        ma.add_new_day(closing_data.iloc[index])

        moving_ave = ma.get_moving_average()
        std_dev = ma.get_standard_deviation()
        band = BollingerBand(moving_ave, std_dev)

        #if the moving average has not been calculate yet, just pass
        if ma.get_moving_average() == 0:
            pass
        #check if moving average has hit the lower bollinger band => buy signal
        elif ma.get_current_close() <= band.lower_band and not has_share:
            shares_owned = amount_current // ma.current_close
            asset_value = shares_owned * ma.current_close
            amount_current -= asset_value
            has_share = True
            to_buy = True
            to_sell = False
        #check if the moving average has hit the upper bollinger band => sell signal
        elif ma.get_current_close() >= band.upper_band and has_share:
            added += shares_owned * ma.get_current_close()
            amount_current += added
            shares_owned = 0
            has_share = False
            to_sell = True
            to_buy = False

        #add all the new values to the collection dictionary
        collection["date"].append(closing_data.index)
        collection["closing_price"].append(closing_data.iloc[index])
        collection["simple_moving_average"].append(ma.moving_average)
        collection["upper_band"].append(band.upper_band)
        collection["lower_band"].append(band.lower_band)
        collection["buy"].append(to_buy)
        collection["sell"].append(to_sell)
        collection["percent_change"].append((amount_current / holdings) * 100)
    
    
    print("-----BACKTEST-----")
    print("Starting Balance in Account: ", holdings)
    print("------------------")
    print("Final Holdings in Account: ", amount_current)
    print("------------------")
    print("Percent Increase/Decrease in Holdings: ", ((amount_current / holdings) * 100) , "%")

    #convert the collections dictionary => pandas dataframe => excel sheet
    data_df = pd.DataFrame.from_dict(collection)
    data_df.to_excel("results.xlsx", index=True)

calculate_bollinger_profit(1000000, close_df)