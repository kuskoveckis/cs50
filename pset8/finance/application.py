import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create BUY TABLE
#db.execute("CREATE TABLE history ( user_id INTEGER, symbol TEXT NOT NULL, shares INTEGER, price NUMERIC NOT NULL, action TEXT, total NUMERIC NOT NULL, date TEXT)")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Current cash
    rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
    current_cash = round(rows[0]["cash"],2)

    # Select stock info
    stocks = db.execute("SELECT symbol, name, SUM(shares) FROM history WHERE user_id = :user_id GROUP BY symbol", user_id = session["user_id"] )

    # Create dict with data
    stock_data = []
    for stock in stocks:
        apis = lookup(stock["symbol"])
        price = apis["price"]
        total_price = price * stock["SUM(shares)"]
        data = {
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": stock["SUM(shares)"],
            "price": price,
            "total": total_price
            }
        stock_data.append(data)

    # Calculate total cash value
    total_cash = current_cash

    for stock in stock_data:
        total_cash = total_cash + stock["total"]

    return render_template("index.html",current_cash=current_cash, stocks=stocks, stock_data=stock_data, total_cash=total_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via GET
    if request.method == "GET":
        return render_template("buy.html")
    # User reached route via POST
    else:
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif lookup(request.form.get("symbol")) == None:
            return apology("must provide correct symbol", 400)
        elif int(request.form.get("shares")) < 1:
            return apology("must provide positive integer", 400)
        else:

            # check for stock price
            smb = lookup(request.form.get("symbol"))

            shares = request.form.get("shares")

            # user's current cash
            rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
            current_cash = rows[0]["cash"]

            # Check if enough cash
            totalPrice = int(shares) * smb["price"]  # price for all shares to buy

            if totalPrice > current_cash:
                return apology("not enough cash", 400)

            # Update user's current cash in database
            current_cash = current_cash - totalPrice
            db.execute("UPDATE users SET cash = :current_cash WHERE id = :user_id",
                        user_id = session["user_id"],
                        current_cash = current_cash)

            db.execute("INSERT INTO history (user_id, symbol, name, shares, price, action, total, date) VALUES (:user_id, :symbol, :name, :shares, :price, :action, :total, :date)",
                        user_id = session["user_id"],
                        symbol = smb["symbol"],
                        name = smb["name"],
                        shares = shares,
                        price = smb["price"],
                        action = "buy",
                        total = totalPrice,
                        date = datetime.datetime.now())
            flash("Bought!")

            return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        data = db.execute("SELECT symbol, action, shares, price, date FROM history WHERE user_id = :user_id ORDER BY date ASC", user_id = session["user_id"] )
        return render_template("history.html",data=data)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via GET
    if request.method == "GET":
        return render_template("quote.html")
    # User reached route via POST
    else:
        return render_template("quoted.html", api=lookup(request.form.get("symbol")))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")
    # User reached route via POST (as by submitting a form via POST)
    else:
        # Query database for username
        used = db.execute("SELECT username FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif used:
            return apology("username already exists", 400)

        # Ensure password and password confirmation was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)
        # Ensure password and password confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match", 400)

        new_username = request.form.get("username")
        password = request.form.get("password")
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        # Insert new user into users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",new_username, hash_password)

        # Redirect user to home page
        flash("Registered!")
        return redirect("/")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Select stock info
    stocks = db.execute("SELECT symbol, name, SUM(shares) FROM history WHERE user_id = :user_id GROUP BY symbol", user_id = session["user_id"])
    # User reached route via GET
    if request.method == "GET":
        # Select stock info
        stocks = db.execute("SELECT symbol, name, SUM(shares) FROM history WHERE user_id = :user_id GROUP BY symbol", user_id = session["user_id"])
        return render_template("sell.html", stocks=stocks)
    # User reached route via POST
    else:
        if not int(request.form.get("shares")):
            return apology("must provide number of shares", 400)
        elif int(request.form.get("shares")) >= 1:
            symbol = request.form.get("symbol")
            for stock in stocks:
                if stock["symbol"] == symbol:
                    current_shares = stock["SUM(shares)"]
            if int(request.form.get("shares")) > current_shares:
                return apology("you don't own enough shares", 400)
            else:
                # Select stock info
                stocks = db.execute("SELECT symbol, name, SUM(shares) FROM history WHERE user_id = :user_id GROUP BY symbol", user_id = session["user_id"])

                # Current cash, stock price, number of shares
                rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
                current_cash = rows[0]["cash"]
                stock_data = lookup(symbol)
                current_price = stock_data["price"]
                shares = request.form.get("shares")

                total_amount = current_price * int(shares)
                current_cash = current_cash + total_amount

                # Update current cash
                db.execute("UPDATE users SET cash = :current_cash WHERE id = :user_id",
                        user_id = session["user_id"],
                        current_cash = current_cash)

                db.execute("INSERT INTO history (user_id, symbol, name, shares, price, action, total, date) VALUES (:user_id, :symbol, :name, :shares, :price, :action, :total, :date)",
                        user_id = session["user_id"],
                        symbol = request.form.get("symbol"),
                        name = stock_data["name"],
                        shares = -int(request.form.get("shares")),
                        price = stock_data["price"],
                        action = "sell",
                        total = total_amount,
                        date = datetime.datetime.now())
                flash("Sold!")

        return redirect("/")
    #return apology("TODO")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add cash"""
    # User reached route via GET
    if request.method == "GET":
        return render_template("add.html")
    # User reached route via POST
    else:
        amount = request.form.get("cash")

        # user's current cash
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
        current_cash = rows[0]["cash"]

        # Update user's current cash in database
        current_cash = current_cash + int(amount)
        db.execute("UPDATE users SET cash = :current_cash WHERE id = :user_id",
            user_id = session["user_id"],
            current_cash = current_cash)

        flash("Cash added!")
        return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
