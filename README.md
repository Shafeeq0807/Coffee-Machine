# Coffee-Machine

A dependency-free coffee machine simulator with a separate domain model and command-line interface. Payments use decimal arithmetic; rejected orders never change inventory or revenue.

## Run locally

```bash
python main.py
python -m unittest discover -s tests -v
```

Requires Python 3.11+.

## Commands

- `menu`: view drinks and prices in USD (preserved from the original project).
- `espresso`, `latte`, `cappuccino`: insert coins and place an order.
- `report`: inspect stock and revenue.
- `refill water 200`: add inventory (milk and coffee also supported).
- `off`: exit gracefully.

The simulation runs in memory; it does not operate hardware or process real payments.

## Development

Changes are checked by GitHub Actions. Keep credentials in environment variables and never commit `.env`, local databases, or build output.
