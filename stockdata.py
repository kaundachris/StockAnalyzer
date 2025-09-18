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
        name = self.stock_data.info.get("longName")
        if name is not None:
            return name
        return "N/A"
    
    # get the company's industry
    def company_industry(self):
        industry = self.stock_data.info.get("industry")
        if industry is not None:
            return industry
        return "N/A"
    
    # get the company's foward PE
    def company_forward_pe(self):
        forward_pe = self.stock_data.info.get("forwardPE")
        if forward_pe is not None:
            return round(forward_pe, 2)
        return 0
    
    # get the company's earnings growth
    def company_earnings_growth(self):
        earnings_growth = self.stock_data.info.get("earningsGrowth")
        if earnings_growth is not None:
            return round(earnings_growth * 100, 2)
        return 0
    
    # get the company's profit margin
    def company_profit_margin(self):
        profit_margin = self.stock_data.info.get("profitMargins")
        if profit_margin is not None:
            return round(profit_margin * 100, 2)
        return 0

    # get the company's market capitalization
    def company_market_cap(self):
        market_cap = self.stock_data.info.get("marketCap")
        if market_cap is not None:
            return market_cap
        return 0
    
    # get the company's price to book value
    def company_book_value(self):
        book_value = self.stock_data.info.get("bookValue")
        if book_value is not None:
            return round(book_value, 2)
        return 0
    
    # get the company's price to book ratio
    def company_pb_ratio(self):
        pb_ratio = self.stock_data.info.get("priceToBook")
        if pb_ratio is not None:
            return round(pb_ratio, 2)
        return 0
    
    # get the company's quick ratio
    def company_quick_ratio(self):
        quick_ratio = self.stock_data.info.get("quickRatio")
        if quick_ratio is not None:
            return round(quick_ratio, 2)
        return 0
    
    # get the company's current ratio
    def company_current_ratio(self):
        current_ratio = self.stock_data.info.get("currentRatio")
        if current_ratio is not None:
            return round(current_ratio, 2)
        return 0
    
    # get the company's free cashflow 
    def company_free_cashflow(self):
        free_cashflow = self.stock_data.info.get("freeCashflow")
        if free_cashflow is not None:
            return round(free_cashflow, 2)
        return 0
