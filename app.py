from flask import Flask, render_template, request, redirect, session
from stockdata import Stock
import bcrypt
import os
import psycopg2
import psycopg2.extras



# check that the password is at least 6 characters long, contains at least one char, and one number
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
        if has_digit and has_letter:
            return True
    return False



# create a database connection
def get_db():
    url = os.environ.get("DATABASE_URL")
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(url)



def initialize_db():
    with get_db() as db:
        cursor = db.cursor()
        # create the users table
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                       id SERIAL PRIMARY KEY,
                       username TEXT NOT NULL UNIQUE,
                       password_hash TEXT NOT NULL)
                       """)
        
        # create the history table
        cursor.execute("""CREATE TABLE IF NOT EXISTS searches(
                       id SERIAL PRIMARY KEY,
                       user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                       ticker TEXT NOT NULL,
                       longName TEXT NOT NULL,
                       industry TEXT NOT NULL,
                       forwardPE REAL,
                       bookValue Real,
                       earningsGrowth REAL,
                       profitMargins REAL,
                       marketCap REAL,
                       priceToBook REAL,
                       quickRatio REAL,
                       currentRatio REAL,
                       freeCashflow REAL,
                       UNIQUE(user_id, longName)
                       )
                       """)
        db.commit()



# formats the numbers into readable format
def format_currency(value):
    if value is None:
        return "N/A"
    return "${:,.2f}".format(value)



# get all the search data to populate the history page
def searches():
    # ensure user is logged in
    if "user_id" not in session:
        return []
    with get_db() as db:
        # get searches related to the user id
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM searches WHERE user_id = %s", (session["user_id"],))
        for item in cursor.fetchall():
            item["freeCashflow"] = format_currency(item["freeCashflow"])
        return cursor.fetchall()

        
    
# to determine which link to show in the navigation
def status():
    if "user_id" in session:
        logged_in = True
    else:
        logged_in = False
    return logged_in



# retreive stock data and store in a usable format
def retrieve_stock_data(ticker:str):
    try:
        stock = Stock(ticker)
    except Exception:
        return None 

    # store the data for rendering
    stock_data = {}
    stock_data["ticker"] = ticker
    stock_data["longName"] = stock.company_name()
    stock_data["industry"] = stock.company_industry()
    stock_data["forwardPE"] = stock.company_forward_pe()
    stock_data["earningsGrowth"] = stock.company_earnings_growth()
    stock_data["profitMargins"] = stock.company_profit_margin()
    stock_data["marketCap"] = stock.company_market_cap()
    stock_data["bookValue"] = stock.company_book_value()
    stock_data["priceToBook"] = stock.company_pb_ratio()
    stock_data["quickRatio"] = stock.company_quick_ratio()
    stock_data["currentRatio"] = stock.company_current_ratio()
    stock_data["freeCashflow"] = stock.company_free_cashflow()
    return stock_data



# store data in database
def store_data(data:dict):
    # store this in the database
    with get_db() as db:
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("DELETE FROM searches WHERE longName = %s AND user_id = %s", (data["longName"], session["user_id"]))
        cursor.execute('''INSERT INTO searches (user_id, ticker, longName, industry, forwardPE, earningsGrowth, profitMargins, marketCap, bookValue, priceToBook, quickRatio, currentRatio, freeCashflow) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                   (session["user_id"], data["ticker"], data["longName"], data["industry"], data["forwardPE"], data["earningsGrowth"], data["profitMargins"], data["marketCap"],
                    data["bookValue"], data["priceToBook"], data["quickRatio"], data["currentRatio"], data["freeCashflow"]))
        db.commit()



app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")
# initialize db at startup (outside __main__)
initialize_db()



@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", logged_in=status()) 

    # get the user's input
    company = request.form.get("user_input")

    #check that it's not empty
    if not company:
            return render_template("index.html", message="No ticker entered. Please enter a valid ticker!", logged_in=status())
    
    # retrieve the data
    stock_data = retrieve_stock_data(company)
    if not stock_data:
        return render_template("index.html", message="Could not find the ticker's data. Please make sure you enter a valid ticker!", logged_in=status())

    # store the search data
    session["last_ticker"] = stock_data["ticker"]

    # to determine which link to show in the navigation

    return render_template("results.html", stock_data=stock_data, logged_in=status())



@app.route("/login", methods=["GET","POST"])
def login():
    # if from other page
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    # check that username field is not empty
    if not username:
        return render_template("login.html", message="Please enter your username!")
    username = username.lower()
    
    # check that the password field is not empty
    password = request.form.get("password")
    if not password:
        return render_template("login.html", message="Please enter your username and password!")
    
    with get_db() as db:
        # check that the username exists in database
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return render_template("login.html", message="You are not registered. Click on the register button above to register!")
        
        # check that the password matches
        if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            return render_template("login.html", message="Invalid password!")
        
        # Set user_id in session after successful login
        session["user_id"] = user["id"]
        return redirect("/history")



@app.route("/register", methods=["GET","POST"])    
def register():
    # if from other page
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    # check that username field is not empty
    if not username:
        return render_template("register.html", message="Please enter your username!")
    username = username.lower()
    
    # check that the password field is not empty
    password = request.form.get("password")
    if not password:
        return render_template("register.html", message="Please enter a password!")
    
    # check that the confirm password field is not empty
    confirm_password = request.form.get("confirm_password")
    if not confirm_password:
        return render_template("register.html", message="Please confirm your password!")
    
    # Check that password is at least 6 characters long and contains letters, digits and characters
    if not check_password(password):
        return render_template("register.html", message="Must contain at least one number and one letter")
    
    if password != confirm_password:
        return render_template("register.html", message="Passwords dont match")

    with get_db() as db:
        # check that the username does not exist in database
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            return render_template("register.html", message="Username exists! Log in please.")
        
        # hash the password
        hash_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # add the user to the database 
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hash_pw.decode("utf-8")))
        db.commit()

        # get user's id
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return render_template("login.html", message="Log in to save your searches" )

        # Set user_id in session after successful login
        session["user_id"] = user["id"]
        return redirect("/history")



@app.route("/history", methods=["GET","POST"])
def history():
    # check that the user is logged in
    if "user_id" not in session:
        return render_template("login.html", message="Log in to save your searches" )
    
    if request.method == "GET":
        # populate the page
        return render_template("history.html", history=searches())
    
    # get the stock stored in the session
    stock = session.get("last_ticker")
    if not stock:
        return render_template("history.html", history=searches())
    
    # retrieve its data
    stock_data = retrieve_stock_data(stock)
    if not stock_data:
        return render_template("history.html", history=searches(), message="Could not find the ticker's data. Please make sure you enter a valid ticker!", logged_in=status())

    # store this in the database
    store_data(stock_data)

    # render the page with the new entry
    return render_template("history.html", history=searches())



@app.route("/update", methods=["POST"])
def update():
    # check that the user is logged in
    if "user_id" not in session:
        return render_template("login.html", message="Log in to save your searches" )
    
    # get the id of the stock to update
    stock_to_update = request.form.get("update")
    if not stock_to_update:
        return render_template("history.html", message="Update failed. Please try again", logged_in=status()) 
    
    # retrieve the data
    stock_data = retrieve_stock_data(stock_to_update)
    if not stock_data:
        return render_template("history.html", history=searches(), message="Could not find the ticker's data. Please make sure you enter a valid ticker!", logged_in=status())

    
    session["last_ticker"] = stock_to_update

    # store this in the database
    store_data(stock_data)

    # render the page with the new entry
    return render_template("history.html", history=searches(), message="Data updated!")



@app.route("/logout", methods=["GET","POST"])
def logout():
    # clear the session data
    session.clear()

    # redirect to the login page
    return redirect("/login")



if __name__ == "__main__":
    app.run()