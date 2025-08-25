import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from dotenv import load_dotenv
import io, csv, datetime as dt

from signals.leo_ingest import build_orders

load_dotenv()
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev")
SIGNAL_DIR = os.getenv("SIGNAL_DIR", "./data/signals")

DEMO_USER = os.getenv("DEMO_USER", "demo")
DEMO_PASS = os.getenv("DEMO_PASS", "demopassword")

app = Flask(__name__)
app.secret_key = SECRET_KEY

def require_login():
    return ("user" in session) and session["user"] == DEMO_USER

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("dashboard") if require_login() else url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip()
        pw    = request.form.get("password","")
        if email == DEMO_USER and pw == DEMO_PASS:
            session["user"] = DEMO_USER
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "error")
    return render_template("login.html")

@app.route("/logout", methods=["POST","GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if not require_login():
        return redirect(url_for("login"))

    # Defaults for first visit
    investable = float(session.get("investable", 1000))
    delta      = float(session.get("delta", 0.0))
    leverage   = float(session.get("leverage", 1.0))
    universe_n = int(session.get("universe_n", 10))
    orders     = []

    if request.method == "POST":
        investable = float(request.form.get("investable", investable))
        delta      = float(request.form.get("delta", delta))
        leverage   = float(request.form.get("leverage", leverage))
        universe_n = int(request.form.get("universe_n", universe_n))

        # clamp
        delta = max(-1.0, min(1.0, delta))
        leverage = max(0.0, min(5.0, leverage))
        if universe_n not in (10,20,30,40,50):
            universe_n = 10

        # persist in session
        session.update(investable=investable, delta=delta, leverage=leverage, universe_n=universe_n)

        # build orders from latest Leo CSV
        try:
            orders = build_orders(SIGNAL_DIR, investable, delta, leverage, universe_n)
        except Exception as e:
            flash(f"Error loading signals: {e}", "error")
            orders = []

    return render_template(
        "dashboard.html",
        investable=investable, delta=delta, leverage=leverage, universe_n=universe_n,
        orders=orders, today=dt.date.today().isoformat()
    )

@app.route("/download_orders.csv", methods=["GET"])
def download_orders_csv():
    if not require_login():
        return redirect(url_for("login"))
    investable = float(session.get("investable", 1000))
    delta      = float(session.get("delta", 0.0))
    leverage   = float(session.get("leverage", 1.0))
    universe_n = int(session.get("universe_n", 10))

    orders = build_orders(SIGNAL_DIR, investable, delta, leverage, universe_n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["symbol","side","signal","ref_price","weight_pct","notional_usd"])
    w.writeheader(); w.writerows(orders)
    mem = io.BytesIO(buf.getvalue().encode("utf-8"))
    mem.seek(0)
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name=f"orders_{dt.date.today().isoformat()}.csv")

if __name__ == "__main__":
    app.run(debug=True)
