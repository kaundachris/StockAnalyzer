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
        if self.stock_data.info["longName"]:
            return self.stock_data.info["longName"]
        return self.ticker
    
    # get the company's industry
    def company_industry(self):
        if self.stock_data.info["industry"]:
            return self.stock_data.info["industry"]
        return "N/A"
    
    # get the company's foward PE
    def company_forward_pe(self):
        if self.stock_data.info["forwardPE"]:
            return round(self.stock_data.info["forwardPE"], 2)
        return 0
    
    # get the company's earnings growth
    def company_earnings_growth(self):
        if self.stock_data.info["earningsGrowth"]:
            return round(self.stock_data.info["earningsGrowth"] * 100, 2)
        return 0
    
    # get the company's profit margin
    def company_profit_margin(self):
        if self.stock_data.info["profitMargins"]:
            return round(self.stock_data.info["profitMargins"] * 100, 2)
        return 0

    # get the company's market capitalization
    def company_market_cap(self):
        if self.stock_data.info["marketCap"]:
            return self.stock_data.info["marketCap"]
        return 0
    
    # get the company's price to book value
    def company_book_value(self):
        if self.stock_data.info["bookValue"]:
            return round(self.stock_data.info["bookValue"], 2)
        return 0
    
    # get the company's price to book ratio
    def company_pb_ratio(self):
        if self.stock_data.info["priceToBook"]:
            return round(self.stock_data.info["priceToBook"], 2)
        return 0
    
    # get the company's quick ratio
    def company_quick_ratio(self):
        if self.stock_data.info["quickRatio"]:
            return round(self.stock_data.info["quickRatio"], 2)
        return 0
    
    # get the company's current ratio
    def company_current_ratio(self):
        if self.stock_data.info["currentRatio"]:
            return round(self.stock_data.info["currentRatio"], 2)
        return 0
    
    # get the company's free cashflow 
    def company_free_cashflow(self):
        if self.stock_data.info["freeCashflow"]:
            return round(self.stock_data.info["freeCashflow"], 2)
        return 0
