import requests

class CompanyLookup():
    def __init__(self):
        # this dictionary is a permernent item of the class
        self.COMPANY_TICKERS = {
            "google": "GOOGL",
            "apple": "AAPL",
            "tesla": "TSLA",
            "nvidia": "NVDA"
        }

        # this is used repeatedly when making calls
        # browser identifier to prevent Yahoo from blocking the request
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }


    # check for existence of company
    def company_exists(self, company_name: str):
        # clean company name
        company_name = company_name.strip().lower()

        # if it looks like a ticker, return it directly
        if len(company_name) < 5:
            return company_name

        # check that it is not in the list of companies already
        # this reduces API calls
        if company_name in self.COMPANY_TICKERS:
            return self.COMPANY_TICKERS.get(company_name)

        # url for the search API for Yahoo Finance
        # go to the search endpoint
        url = "https://query2.finance.yahoo.com/v1/finance/search"

        # pass the company who's data you want retrieved
        parameters = {
            # what company details you want to pull 
            "q": company_name,
            # without this, the call will return several quotes. This minimizes the quotes
            "quotesCount": 5,
            # without this, the call will return several news results. This minimizes the news results
            "newsCount": 0,
        }

        # make the actual call to the API
        response = requests.get(url, params=parameters, headers=self.headers)

        # check for a response
        """
            2xx  →  Success
            3xx  →  Redirect (the resource moved somewhere else)
            4xx  →  Your fault (bad request, not found, not authorised)
            5xx  →  Their fault (server crashed, overloaded)
        """
        if response.status_code != 200:
            raise ConnectionError(f"API returned {response.status_code}")
        
        # store the response in JSON format for readability
        data = response.json()

        # check the data for ticker, return an empty list if missing
        quotes = data.get("quotes", [])

        if quotes:
            # the first list in quotes is the priority
            # store the company and ticker into the dictionary
            ticker = quotes[0].get("symbol")
            self.COMPANY_TICKERS[company_name] = ticker
            return ticker
        return None