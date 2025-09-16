#import the yfinance ticker
from yfinance import Ticker
import pandas as pd

class Stock():
    def __init__(self, ticker:str):
        self.ticker = ticker
        self._stock_data = None

    #set the property so that the data is called and stored into cache - reduces the calls to the API
    @property
    def stock_data(self):
        if self._stock_data is None:
            self._stock_data = Ticker(self.ticker)
        return self._stock_data
    
    # Get the company's name
    def company_name(self):
        return self.stock_data.info["longName"]
    
    # get the company's industry
    def company_industry(self):
        return self.stock_data.info["industry"]
    
    # get the company's foward PE
    def company_forward_pe(self):
        return round(self.stock_data.info["forwardPE"], 2)
    
    # get the company's earnings growth
    def company_earnings_growth(self):
        return round(self.stock_data.info["earningsGrowth"] * 100, 2)
    
    # get the company's profit margin
    def company_profit_margin(self):
        return round(self.stock_data.info["profitMargins"] * 100, 2)

    # get the company's market capitalization
    def company_market_cap(self):
        return self.stock_data.info["marketCap"]
    
    # get the company's price to book value
    def company_book_value(self):
        return round(self.stock_data.info["bookValue"], 2)
    
    # get the company's price to book ratio
    def company_pb_ratio(self):
        return round(self.stock_data.info["priceToBook"], 2)
    
    # get the company's quick ratio
    def company_quick_ratio(self):
        return round(self.stock_data.info["quickRatio"], 2)
    
    # get the company's current ratio
    def company_current_ratio(self):
        return round(self.stock_data.info["currentRatio"], 2)
    
    # get the company's free cashflow 
    def company_free_cashflow(self):
        return round(self.stock_data.info["freeCashflow"], 2)
    

gfdaa = Stock("gfdaa")
print(gfdaa.company_free_cashflow())