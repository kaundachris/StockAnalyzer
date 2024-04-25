import yfinance as yf
import pandas as pd


class Financials:
    def __init__(self, ticker: str):
        """Instantiates the stock whose data you need"""
        self.ticker = ticker

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, ticker):
        if pd.DataFrame(yf.Ticker(ticker).income_stmt).empty:
            raise NameError('Please enter a valid stock ticker')
        else:
            self._ticker = ticker

    def stock(self):
        """Passes the ticker to the yfinance module to retrieve data"""
        return yf.Ticker(self.ticker)

    def income_statement(self):
        """

        Retrieves the income statement information
        Passes the information into a data frame
        :rtype: Dataframe
        """
        income_stmt = pd.DataFrame(self.stock().income_stmt)
        return income_stmt

    def balance_sheet(self):
        """

        Retrieves the balance sheet information
        Passes the information into a data frame
        :rtype: Dataframe
        """
        balance_sht = pd.DataFrame(self.stock().balance_sheet)
        return balance_sht

    def cash_flow(self):
        """

        Retrieves the cash flow information
        Passes the information into a data frame
        :return: Dataframe of performance
        :rtype: Dataframe
        """
        cashflow = pd.DataFrame(self.stock().cash_flow)
        return cashflow

    def write_all_data(self):
        """

        Sets the path for to which data is to be written
        Uses excelwriter to write the data to an Excel sheet
        :return: Done if no issue detected
        :rtype: str
        """
        path = f'C:\\Users\\chris\\Documents\\Financial Independence\\{self.ticker}.xlsx'
        with pd.ExcelWriter(path) as writer:
            self.income_statement().to_excel(writer, 'Financials')
            self.balance_sheet().to_excel(writer, 'Balance Sheet')
            self.cash_flow().to_excel(writer, 'Cash Flow')
        return 'Done'
