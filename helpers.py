"""
    offloads some of the initializers on the app.py file here
    leave app.py purely for the routes
    reduces the size of the app.py file
    allows for easy skimming of app.py
"""

#import dependencies
import psycopg2
import psycopg2.extras
import os
from flask import session

from company_check import CompanyLookup
from stockdata import Stock


# create a database connection
def get_db():
    # environment variable used to protect the actual database location from attackers
    connection = psycopg2.connect(os.environ["DATABASE_URL"])

    # commit any changes automatically
    connection.autocommit = True

    return connection


# create the database with all the fields needed
def initialize_db():
    # open connection to database
    connection = get_db()

    with connection.cursor() as db:
        # create the users table
        db.execute("""CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL)
                """)

        # create the history table
        db.execute("""CREATE TABLE IF NOT EXISTS searches(
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                ticker TEXT NOT NULL,
                long_name TEXT NOT NULL,
                industry TEXT NOT NULL,
                forward_pe REAL,
                book_value Real,
                earnings_growth REAL,
                profit_margins REAL,
                market_cap REAL,
                price_book REAL,
                quick_ratio REAL,
                current_ratio REAL,
                free_cashflow REAL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                UNIQUE(user_id, long_name)
                )""")
    
    # close connection to database
    connection.close()


# retreive stock data and store in a usable format
def retrieve_stock_data(ticker: str):
    # check that the company exists
    company_exists = CompanyLookup().company_exists(ticker)

    # if it does not, return None
    if not company_exists:
        return None

    # if it does, proceed to get the data
    stock = Stock(company_exists)
    
    try:
        # store the data for rendering
        stock_data = {}
        stock_data["ticker"] = ticker
        stock_data["long_name"] = stock.company_name
        stock_data["industry"] = stock.company_industry
        stock_data["forward_pe"] = stock.company_forward_pe
        stock_data["earnings_growth"] = stock.company_earnings_growth
        stock_data["profit_margins"] = stock.company_profit_margin
        stock_data["market_cap"] = stock.company_market_cap
        stock_data["book_value"] = stock.company_book_value
        stock_data["price_book"] = stock.company_pb_ratio
        stock_data["quick_ratio"] = stock.company_quick_ratio
        stock_data["current_ratio"] = stock.company_current_ratio
        stock_data["free_cashflow"] = stock.company_free_cashflow
        stock_data["price_chart"] = stock.price_chart
        return stock_data
    except Exception:
        return None


# store data in database
def store_data(data: dict):
    # store this in the database
    connection = get_db()
    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
        db.execute("DELETE FROM searches WHERE long_name = %s AND user_id = %s",
                (data["long_name"], session["user_id"]))
        db.execute('''INSERT INTO searches (user_id, ticker, long_name, industry, forward_pe, earnings_growth, profit_margins, market_cap, book_value, price_book, quick_ratio, current_ratio, free_cashflow)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (session["user_id"], data["ticker"], data["long_name"], data["industry"], data["forward_pe"], data["earnings_growth"], data["profit_margins"], data["market_cap"],
                    data["book_value"], data["price_book"], data["quick_ratio"], data["current_ratio"], data["free_cashflow"]))
    connection.close()


# to determine which link to show in the navigation (login, logout, register)
def status():
    if "user_id" in session:
        return True
    else:
        return False


# check that the password meets security requirements
def check_password(password):
    has_digit = False
    has_letter = False

    # check that the password is at least 6 character long
    if len(password) < 6:
        return False

    # check that the password has a number and letter
    for char in password:
        if char.isdigit():
            has_digit = True
        elif char.isalpha():
            has_letter = True

        ## if both of the above are true, exit early (saves time)
        if has_digit and has_letter:
            return True
    return False


# get all the search data to populate the history page
def searches(sort_by=None, order="ASC"):
    # ensure user is logged in
    if "user_id" not in session:
        return []
    
    # whitelist of sortable columns (prevents SQL injection)
    valid_columns = [
        "forward_pe", "earnings_growth", "profit_margins",
        "price_book", "quick_ratio", "current_ratio", "free_cashflow"
    ]

    # whitelist of allowable orders (prevents SQL injection)
    valid_orders = ["ASC", "DESC"]


    # validate the sort item selected
    if sort_by not in valid_columns:
        sort_by = None

    # set the order item to "ASC" always
    if order not in valid_orders:
        order = "ASC"

    #connect to database
    connection = get_db()

    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
        # get searches related to the user id
        if sort_by:
            # if sort parameter present, sort the results
            query = f"SELECT * FROM searches WHERE user_id = %s ORDER BY {sort_by} {order} NULLS LAST"
            db.execute(query, (session["user_id"],))
        else:
            # if search parameter missing, return results as is
            db.execute("SELECT * FROM searches WHERE user_id = %s", (session["user_id"],))
        searches = db.fetchall()

        # close connection to database
        connection.close()

        return searches
