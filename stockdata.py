#import the yfinance ticker
from yfinance import Ticker


class Stock():
    def __init__(self, ticker:str):
        self.ticker = ticker
        self._info = None

    #set the property so that the data is called and stored into cache - reduces the calls to the API
    @property
    def info(self):
        # if stockdata already exists, cache it to reduce API calls
        if self._info is not None:
            return self._info

        # checks for data
        # first, call the API for data
        stock = Ticker(self.ticker)

        # store data, if any
        data = stock.history(period="1d")
        
        # if no data, raise ValueError. 
        if data.empty:
            raise ValueError(f"Data for {self.ticker} could not be found")
        
        self._info = stock.info
        return self._info
    

    # Repeated pattern of accessing information on stock ofloaded to this function
    def _get_info(self, key):
        return self.info.get(key)
   
    # Get the company's name
    def company_name(self):
        return self._get_info("longName") or "N/A" 
    
    # get the company's industry
    def company_industry(self):
        return self._get_info("industry") or "N/A" 
    
    # get the company's foward PE
    def company_forward_pe(self):
        forwardPE = self._get_info("forwardPE")
        if forwardPE is not None:
            return round(forwardPE, 2)
        else:
            return 0
    
    # get the company's earnings growth
    def company_earnings_growth(self):
        earnings_growth = self.info.get("earningsGrowth")
        if earnings_growth is not None:
            return round(earnings_growth * 100, 2)
        return 0
    
    # get the company's profit margin
    def company_profit_margin(self):
        profit_margin = self.info.get("profitMargins")
        if profit_margin is not None:
            return round(profit_margin * 100, 2)
        return 0

    # get the company's market capitalization
    def company_market_cap(self):
        market_cap = self.info.get("marketCap")
        if market_cap is not None:
            return market_cap
        return 0
    
    # get the company's price to book value
    def company_book_value(self):
        book_value = self.info.get("bookValue")
        if book_value is not None:
            return round(book_value, 2)
        return 0
    
    # get the company's price to book ratio
    def company_pb_ratio(self):
        pb_ratio = self.info.get("priceToBook")
        if pb_ratio is not None:
            return round(pb_ratio, 2)
        return 0
    
    # get the company's quick ratio
    def company_quick_ratio(self):
        quick_ratio = self.info.get("quickRatio")
        if quick_ratio is not None:
            return round(quick_ratio, 2)
        return 0
    
    # get the company's current ratio
    def company_current_ratio(self):
        current_ratio = self.info.get("currentRatio")
        if current_ratio is not None:
            return round(current_ratio, 2)
        return 0
    
    # get the company's free cashflow 
    def company_free_cashflow(self):
        free_cashflow = self.info.get("freeCashflow")
        if free_cashflow is not None:
            return round(free_cashflow, 2)
        return 0