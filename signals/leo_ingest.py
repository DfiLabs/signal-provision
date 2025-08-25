from pathlib import Path
import pandas as pd


def pick_latest_csv(signals_dir: str) -> Path:
    p = Path(signals_dir)
    candidates = sorted(p.glob("*.csv"), key=lambda x: x.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"No CSV files in {signals_dir}")
    return candidates[-1]


def load_latest(signals_dir: str) -> pd.DataFrame:
    f = pick_latest_csv(signals_dir)
    df = pd.read_csv(f)
    # Expect columns like: ticker, target_notional, ref_price, ...
    df["ticker"] = df["ticker"].str.replace("_", "", regex=False).str.upper()
    df["abs_notional"] = df["target_notional"].abs()
    return df[["ticker","target_notional","abs_notional","ref_price"]].dropna()


def build_orders(signals_dir: str, amount: float, delta: float, leverage: float, universe_n: int):
    """
    amount: investable USD >=0
    delta:  [-1..+1]  (-1 full short, 0 neutral, +1 full long)
    leverage: >=0
    universe_n: {10,20,30,40,50} (split half long / half short)
    """
    df = load_latest(signals_dir)
    longs  = df[df["target_notional"] > 0].sort_values("target_notional", ascending=False)
    shorts = df[df["target_notional"] < 0].sort_values("abs_notional",  ascending=False)

    k = max(1, min(universe_n // 2, len(longs), len(shorts)))
    longs  = longs.head(k).copy()
    shorts = shorts.head(k).copy()

    gross = max(0.0, amount) * max(0.0, leverage)
    long_cap  = gross * (delta + 1.0) / 2.0
    short_cap = gross * (1.0 - delta) / 2.0

    # Weights within each side proportional to Leo's notionals
    long_w  = longs["target_notional"] / max(1e-12, longs["target_notional"].sum())
    short_w = shorts["abs_notional"]  / max(1e-12, shorts["abs_notional"].sum())

    orders = []
    for (sym, sig, price), w in zip(longs[["ticker","target_notional","ref_price"]].itertuples(index=False), long_w):
        notional = float(long_cap * float(w))
        orders.append({"symbol": sym, "side": "Buy", "signal": float(sig),
                       "ref_price": float(price), "weight_pct": round(100*notional/gross, 3) if gross else 0.0,
                       "notional_usd": round(notional, 2)})

    for (sym, sig, price), w in zip(shorts[["ticker","target_notional","ref_price"]].itertuples(index=False), short_w):
        notional = float(short_cap * float(w))
        orders.append({"symbol": sym, "side": "Sell", "signal": float(sig),
                       "ref_price": float(price), "weight_pct": round(100*notional/gross, 3) if gross else 0.0,
                       "notional_usd": round(notional, 2)})

    # Sort for UX: buys first by size desc, then sells by size desc
    return sorted(orders, key=lambda x: (x["side"] != "Buy", -x["notional_usd"]))
