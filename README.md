# StockFundamentalsExtracter
Get the specific stock data you need in an excel file.

Description:
This engine takes the company’s ticker (for publicly traded companies) as the argument. It passes the ticker onto the finance module to retrieve up to date information. The information related to the income statement, the balance sheet, and the cash flow statement is then stored in data frames for easy analysis. It then takes the data frame information and extracts specific data that can be used to calculate the liquidity, margins and cash flow generation of the company in question.

Modules Used:
yfinance
pandas
