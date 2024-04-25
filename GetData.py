import pandas as pd

from Extract_Financials import Financials


class GetSpecificData:
    """
    Instantiates the stock whose data I need
    """
    def __init__(self, stock: str):
        self.stock = stock

    """
    Checks that the stock is valid
    """
    def ticker(self):
        return Financials(self.stock)

    """
    Extracts the most recent data in relation to Revenue and Operating Income
    :rtype: Dictionary
    """
    def get_margin_data(self):
        stmt_performance = self.ticker().income_statement()
        total_revenue = pd.DataFrame(stmt_performance.loc['Total Revenue'])
        operating_income = pd.DataFrame(stmt_performance.loc['Operating Income'])
        net_income = pd.DataFrame(stmt_performance.loc['Net Income'])
        margin_data = pd.concat([total_revenue.transpose(), operating_income.transpose(), net_income.transpose()])
        return margin_data

    """
    Extracts the most recent data in relation to Total Assets, Goodwill and Total Debt
    :rtype: Dictionary
    """
    def get_ltdebt_data(self):
        stmt_position = self.ticker().balance_sheet()
        total_assets = pd.DataFrame(stmt_position.loc['Total Assets'])
        goodwill = pd.DataFrame(stmt_position.loc['Goodwill'])
        total_debt_net_mi = pd.DataFrame(stmt_position.loc['Total Liabilities Net Minority Interest'])
        ltdebt_data = pd.concat([total_assets.transpose(), goodwill.transpose(), total_debt_net_mi.transpose()])
        return ltdebt_data

    """
    Extracts the most recent data in relation to Current Assets and Current Liabilities
    :rtype: Dictionary
    """
    def get_stdebt_data(self):
        stmt_position = self.ticker().balance_sheet()
        current_assets = pd.DataFrame(stmt_position.loc['Current Assets'])
        current_liabilities = pd.DataFrame(stmt_position.loc['Current Liabilities'])
        stdebt_data = pd.concat([current_assets.transpose(), current_liabilities.transpose()])
        return stdebt_data

    """
    Extracts the most recent data in relation to Total Cash from Operating Activities and Capital Expenditure
    :rtype: Dictionary
    """
    def get_cashflow_data(self):
        stock = self.ticker()
        stmt_cashflow = stock.cash_flow()
        total_cash_opex = pd.DataFrame(stmt_cashflow.loc['Cash Flow From Continuing Operating Activities'])
        capital_exp = pd.DataFrame(stmt_cashflow.loc['Capital Expenditure'])
        cashflow_data = pd.concat([total_cash_opex.transpose(), capital_exp.transpose()])
        return cashflow_data

    """

            Sets the path for to which data is to be written
            Uses excelwriter to write the data to an Excel sheet
            :return: Done if no issue detected
            :rtype: str
            """
    def write_specific_data(self):
        path = f'C:\\Users\\chris\\Documents\\Financial Independence\\{self.stock}.xlsx'
        data = pd.concat(
            [self.get_margin_data(), self.get_ltdebt_data(), self.get_stdebt_data(), self.get_cashflow_data()]
        )
        with pd.ExcelWriter(path) as writer:
            data.to_excel(writer, sheet_name='Stock Data')
        return 'Done'
