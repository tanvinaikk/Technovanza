import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///autism.db")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set the secret key to some random bytes. Keep this really secret!
_mail_enabled = os.environ.get("MAIL_ENABLED", default="true")
MAIL_ENABLED = _mail_enabled.lower() in {"1", "t", "true"}

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Continuation of homepage maybe"""
    if request.method == "GET":
        return render_template("index.html")
    


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via GET (as by clicking a link or via redirect -> display registration form)
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":

        # Validate submission
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password and password confirmation were submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("password confirmation required", 403)

        # Ensure password and password confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and password confirmation must match")

        # Hash password
        hash = generate_password_hash(request.form.get("password"))

        # Add UNIQUE user to database
        try:
            result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)
        except:
            # Ensure username is unique
            return apology("username is already registered")

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to login form
        return redirect("/")


@app.route("/emotions", methods=["GET", "POST"])
@login_required
def emotions():
    """Recognize and practice emotions"""
        if request.method == "GET":
        return render_template("index..html")
    return apology("TODO")


@app.route("/todos", methods=["GET", "POST"])
@login_required
def todos():
    """Reminder of your everyday todo"""
    return apology("TODO")


@app.route("/gamify", methods=["GET", "POST"])
@login_required
def gamify():
    """Play some games"""
    return apology("TODO")


@app.route("/guide", methods=["GET", "POST"])
@login_required
def guide():
    """A guide for Caregivers"""
    return apology("TODO")


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    """To keep a note of behavioural patterns"""
    return apology("TODO")


@app.route("/progress", methods=["GET", "POST"])
@login_required
def progress():
    """Records Progress of User"""
    return apology("TODO")
