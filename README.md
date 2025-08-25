# SignalPulse

SignalPulse is a modular web application for delivering crypto factor signals to retail users.  It allows investors to adjust their investable amount and tilt the strategy long, short or neutral via intuitive sliders, then presents a table of daily orders derived from the latest signals.

## Features

* **Web terminal** – A responsive interface built with Flask and Jinja templates.  Users log in, set an investable amount and choose a portfolio delta (–±1 for full short, 0 for market neutral, +1 for full long).
* **Daily orders** – The dashboard displays a table of orders based on the chosen parameters.  In this skeleton the orders are synthetic; in production they would be generated from proprietary signals.
* **Modern design** – Custom CSS (`static/css/style.css`) provides a clean layout, and a bespoke logo (`static/images/logo.png`) embodies the SignalPulse brand.
* **Extensible architecture** – The code is intentionally simple so you can extend it with database storage, API endpoints, or additional analytics.

## Commercial offering

SignalPulse is intended to mirror the style of professional factor platforms like Unravel Finance.  A commercial package would include:

| Service | Description |
|---|---|
| **Factor portfolios** | Market‑neutral multi‑factor portfolios combining momentum, value, liquidity and other factors【403211691097761†screenshot】. |
| **Signal variants** | Access to signals with different cross‑sectional and time‑series biases (long‑only, short‑only, neutral). |
| **Unique datasets** | Proprietary datasets such as liquidity, orderbook‑derived, flow, on‑chain and sentiment signals【403211691097761†screenshot】. |
| **Web terminal** | A modern web terminal where users can set their investable amount, choose delta and execute daily orders. |

> **Legal notice**: SignalPulse is developed by a DFI entity.  The information provided is for educational and informational purposes only and does not constitute investment advice.  Always consult a qualified professional before making investment decisions.

## Getting started

1. **Install dependencies** – Run `pip install flask werkzeug` to install the required Python packages.
2. **Run the application** – Execute `python app.py` from the project root.  The app listens on `http://localhost:5000` by default.
3. **Log in** – Visit the app in your browser and sign in with the default credentials (`demo` / `demopassword`).  These are hard‑coded for demonstration; integrate a proper authentication system for production.

## Roadmap

* **Data integration** – Connect the app to your research instance to fetch live signal files instead of using dummy data.
* **User management** – Implement registration, password storage and role‑based access control.
* **Programmatic API** – Provide endpoints for algorithmic execution and external clients.
* **Analytics** – Add performance charts, backtest statistics and order history to the dashboard.

---

This repository is provided as an illustrative starting point and is licensed under the MIT licence.
