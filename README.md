# Stock Support Tool

A personal research project that explores whether a simple, disciplined machine-learning system can rank diversified ETFs and estimate their risk using only information available at each decision time.

This project is a decision-support experiment, not an autonomous trading system. It will produce monthly research recommendations for manual review and will be compared with simple passive and systematic benchmarks after estimated trading costs.

## Learning path

1. Freeze the research question and evaluation rules.
2. Audit the Yahoo Finance data before engineering features.
3. Build passive and momentum baselines.
4. Implement chronological walk-forward evaluation.
5. Train a simple return-ranking model.
6. Add a separate volatility model and deterministic risk rules.
7. Stress-test the frozen system.
8. Run it in shadow or paper mode before considering any personal use.

## Current step

Read [`research_charter.md`](research_charter.md). Change any assumption you genuinely disagree with now. Once model results have been viewed, the frozen choices in that file must not be changed to improve the backtest.

## Data policy

- Yahoo Finance via `yfinance` is used only for this private, educational project.
- Raw downloads will be preserved locally with fetch metadata.
- Historical execution prices and total-return calculations will be kept separate.
- Any current value used for a real decision must be checked against the brokerage account.
- The downloaded Yahoo data will not be redistributed from this repository.

