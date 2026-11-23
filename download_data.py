"""Download and check the market data used by this project."""

from pathlib import Path

import pandas as pd
import yfinance as yf


SYMBOLS = ["SPY", "AAPL", "MSFT"]
START_DATE = "2015-01-01"
OUTPUT_DIRECTORY = Path("data/raw")
REQUIRED_COLUMNS = ["Open", "High", "Low", "Close"]


def download_symbol(symbol: str) -> pd.DataFrame:
    """Download unadjusted daily prices and corporate actions for one symbol."""
    return yf.Ticker(symbol).history(
        start=START_DATE,
        interval="1d",
        auto_adjust=False,
        actions=True,
    )


def validate_data(data: pd.DataFrame, symbol: str) -> None:
    """Stop with a clear error if downloaded data does not look reasonable."""
    if data.empty:
        raise ValueError(f"{symbol}: no data was downloaded")

    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError(f"{symbol}: dates are not stored as a DatetimeIndex")

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"{symbol}: missing required columns: {missing}")

    if not data.index.is_monotonic_increasing:
        raise ValueError(f"{symbol}: dates are not in order")

    if data.index.has_duplicates:
        raise ValueError(f"{symbol}: duplicate dates were found")

    if data[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError(f"{symbol}: a price value is missing")

    if (data["High"] < data["Low"]).any():
        raise ValueError(f"{symbol}: a daily high is below its daily low")


def save_data(data: pd.DataFrame, symbol: str) -> Path:
    """Save one symbol to a CSV file and return its path."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIRECTORY / f"{symbol}.csv"

    # Daily prices only need a calendar date, not a time-zone offset.
    data_to_save = data.copy()
    if data_to_save.index.tz is not None:
        data_to_save.index = data_to_save.index.tz_localize(None)

    data_to_save.to_csv(
        output_path,
        index_label="Date",
        date_format="%Y-%m-%d",
    )
    return output_path


def main() -> None:
    for symbol in SYMBOLS:
        print(f"Downloading {symbol}...")
        data = download_symbol(symbol)
        validate_data(data, symbol)
        output_path = save_data(data, symbol)

        first_date = data.index[0].date()
        last_date = data.index[-1].date()
        print(
            f"Saved {len(data):,} rows ({first_date} to {last_date}) "
            f"to {output_path}"
        )

    print("Step 1 complete.")


if __name__ == "__main__":
    main()
