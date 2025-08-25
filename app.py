from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

"""
app.py
~~~~~~~~

SignalPulse skeleton web application.

This Flask app provides a simple demonstration of how a factor‑signal platform might
be organised.  It implements a basic login system using a single hardcoded user,
displays a dashboard where the user can select an investable amount and
portfolio delta via sliders, and presents a table of dummy orders.  In a
production system, user authentication, data storage and signal generation
would be handled by proper databases and secure APIs.  Here we focus on the
layout and flow of the UI to illustrate the concept.

To run this app locally, install Flask (``pip install flask``) and run
``python app.py`` then visit ``http://localhost:5000`` in your browser.

This code is released under the MIT licence.
"""

# Create the Flask application
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure random secret in production

###############################################################################
# Dummy user management
###############################################################################
# In a real application you would store users in a database and hash their
# passwords.  For this skeleton we hardcode a single user.
USERS = {
    "demo": generate_password_hash("demopassword")
}


def is_logged_in() -> bool:
    """Return True if the current session is authenticated."""
    return bool(session.get("user"))


###############################################################################
# Routes
###############################################################################
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle the login form and redirect to dashboard when successful."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        stored_hash = USERS.get(username)
        if stored_hash and check_password_hash(stored_hash, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "error")
    if is_logged_in():
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log the user out by clearing the session."""
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """Display the dashboard with sliders and dummy orders."""
    if not is_logged_in():
        return redirect(url_for("login"))

    # Default values for the sliders
    investable = request.form.get("investable_amount", 100000)  # default 100k
    delta = request.form.get("delta", 0)
    try:
        investable = float(investable)
        delta = float(delta)
    except ValueError:
        investable = 100000
        delta = 0

    # Generate dummy orders based on the delta.  In reality you'd fetch the
    # latest orders from your research instance or database.
    orders = generate_dummy_orders(investable, delta)

    return render_template(
        "dashboard.html",
        investable=investable,
        delta=delta,
        orders=orders,
    )


###############################################################################
# Helper functions
###############################################################################
def generate_dummy_orders(investable: float, delta: float) -> list:
    """Return a list of dummy order dictionaries.

    This function synthesises a set of orders based on the investable amount and
    the chosen delta (portfolio tilt).  A positive delta biases towards long
    positions, a negative delta biases towards short positions, and zero is
    market neutral.
    """
    # Example asset universe
    assets = ["BTC", "ETH", "SOL", "BNB", "XRP"]
    orders = []
    # Spread capital equally across assets and modulate by delta
    base_position = investable / len(assets)
    for asset in assets:
        # A simple factor determines the quantity sign based on delta
        qty_factor = delta if delta != 0 else 1
        # The order size (not realistic; demonstration only)
        qty = round(qty_factor * base_position / 10000, 4)
        # Determine buy/sell
        side = "Buy" if qty > 0 else "Sell"
        orders.append({
            "asset": asset,
            "side": side,
            "quantity": abs(qty),
        })
    return orders


if __name__ == "__main__":
    # Run the app in debug mode for development
    app.run(debug=True)
