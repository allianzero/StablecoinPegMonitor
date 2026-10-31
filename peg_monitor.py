"""Stablecoin peg monitor.

Fetches USD prices for common stablecoins (CoinGecko by default, or
any callable you inject for tests), computes each coin's deviation
from $1, and classifies it as OK, WATCH, or ALERT. It only reports;
it never trades.
"""
import argparse
import json
import sys

import requests

STABLECOINS = {
    "USDT": "tether",
    "USDC": "usd-coin",
    "DAI": "dai",
    "FDUSD": "first-digital-usd",
    "USDe": "ethena-usde",
}


def fetch_prices():
    ids = ",".join(STABLECOINS.values())
    resp = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": ids, "vs_currencies": "usd"},
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    prices = {}
    for symbol, coin_id in STABLECOINS.items():
        if coin_id in data:
            prices[symbol] = float(data[coin_id]["usd"])
    return prices


def deviation_pct(price):
    return (price - 1.0) * 100


def assess(price, watch_pct=0.5, alert_pct=2.0):
    dev = abs(deviation_pct(price))
    if dev > alert_pct:
        return "ALERT"
    if dev > watch_pct:
        return "WATCH"
    return "OK"


def monitor(prices):
    rows = []
    for symbol, price in prices.items():
        rows.append({
            "symbol": symbol, "price_usd": price,
            "deviation_pct": deviation_pct(price),
            "status": assess(price),
        })
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description="Stablecoin peg monitor")
    parser.add_argument("--prices", default="", help="Optional JSON prices for offline mode")
    args = parser.parse_args(argv)
    try:
        prices = json.loads(args.prices) if args.prices else fetch_prices()
        rows = monitor({k.upper(): float(v) for k, v in prices.items()})
    except Exception as exc:  # noqa: BLE001 - CLI should report, not crash
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"rows": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
