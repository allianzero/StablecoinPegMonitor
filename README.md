# StablecoinPegMonitor

A Python tool that monitors how far common stablecoins deviate from their $1 peg, using CoinGecko prices, and classifies each coin as OK, WATCH, or ALERT.

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.9 or later.

## Usage

Live prices:

```bash
python peg_monitor.py
```

Offline mode with prices you supply:

```bash
python peg_monitor.py --prices '{"USDT": 1.0, "DAI": 0.95}'
```

Example output:

```json
{
  "rows": [
    {"symbol": "USDT", "price_usd": 1.0, "deviation_pct": 0.0, "status": "OK"},
    {"symbol": "DAI", "price_usd": 0.95, "deviation_pct": -5.0, "status": "ALERT"}
  ]
}
```

## How it works

- Deviation = `(price - 1.0) * 100` percent.
- Status: OK when deviation is at most 0.5%, WATCH when above 0.5% up to 2%, ALERT when above 2%.
- Tracked coins: USDT, USDC, DAI, FDUSD, and USDe.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests use supplied prices, so they run offline.

## Limitations

- Prices are point-in-time snapshots from a public API and can be rate-limited.
- A peg warning is information only, not financial advice and not a trading signal.
- This tool never trades and never needs a private key.

## License

MIT. See `LICENSE`.
