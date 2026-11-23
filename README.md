# Stock Investment Tool

A personal tool that uses stock-market data to help me make better investment decisions.

## What it will do

1. Download market data from Yahoo Finance.
2. Analyze price trends and risk.
3. Use machine learning to score stocks and ETFs.
4. Show the strongest choices in a simple dashboard.
5. Test past recommendations before I use them personally.

The tool will provide information and suggestions. I will make the final investment decisions myself.

## First version

The first version will:

- Use daily market data.
- Analyze a small list of stocks and ETFs.
- Predict whether each investment is likely to perform well over the next month.
- Rank the choices from strongest to weakest.
- Show expected risk alongside each score.
- Track how the suggestions would have performed in the past.

## Build order

1. Download and inspect market data.
2. Create useful indicators from the data.
3. Build a simple prediction model.
4. Test the model on older market data.
5. Build a dashboard.
6. Track its suggestions without investing money first.

## Run Step 1

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python download_data.py
```

This downloads daily data for SPY, AAPL, and MSFT into `data/raw/`.

