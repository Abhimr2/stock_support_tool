# Research Charter — Version 1

Status: **DRAFT — review before locking**

## 1. Research question

Using only information available after each month-end close, can a calibrated machine-learning model rank a fixed group of liquid ETFs well enough that a simple, long-only portfolio outperforms equal weighting and basic momentum after estimated trading costs?

The system is for personal research and manual decision support. It will not place live orders autonomously.

## 2. Research universe

The scored universe is fixed before any results are viewed:

| Exposure | Symbol |
| --- | --- |
| U.S. large-cap stocks | SPY |
| U.S. small-cap stocks | IWM |
| Developed international stocks | EFA |
| Emerging-market stocks | EEM |
| Intermediate U.S. Treasuries | IEF |
| Long U.S. Treasuries | TLT |
| Investment-grade corporate bonds | LQD |
| U.S. real estate | VNQ |
| Gold | GLD |
| Broad commodities | DBC |

SHY is reserved as the defensive asset and is not scored against the ten risk assets.

This fixed ETF universe is a learning simplification. It does not eliminate selection bias and must not be described as a historically complete stock universe.

## 3. Decision and execution timing

- Features are observed after the official close on the final trading day of each month.
- A simulated trade may execute no earlier than the next trading day's open.
- Positions are held until the next monthly rebalance.
- There is no intramonth trading in version 1.

## 4. Prediction targets

### Return target

For every ETF and month, calculate the total return over the next holding interval. The classification label is:

```text
1 if the ETF's forward total return exceeds the cross-sectional median
  of the ten scored ETFs for that month
0 otherwise
```

The model outputs the probability of outperforming that median. Probabilities are used to rank ETFs; they are not interpreted as guaranteed profits.

### Risk target

Predict annualized realized volatility over the same forward holding interval. Return ranking and risk forecasting remain separate problems.

## 5. Allowed feature families

Version 1 may use only:

- 1-, 3-, 6-, and 12-month returns
- 1- and 3-month realized volatility
- Drawdown from the trailing one-year high
- Distance from moving averages
- Recent volume change
- Relative strength versus SPY
- Rolling correlation with SPY

News, social sentiment, fundamentals, macroeconomic releases, options data, and intraday data are excluded from version 1.

## 6. Model families

- Return baseline: L2-regularized logistic regression
- Return challenger: shallow LightGBM classifier
- Risk baseline: trailing historical volatility
- Risk challenger: ridge regression or shallow LightGBM regressor

Neural networks and reinforcement learning are excluded from version 1.

## 7. Portfolio policy

At each rebalance:

1. An ETF is eligible if its predicted outperformance probability is at least 0.55.
2. It is rejected if predicted volatility is above its training-window 90th percentile.
3. Select up to four eligible ETFs with the highest probabilities.
4. Assign 25% to each selected slot.
5. Assign unused slots to SHY.
6. Remain long-only, unlevered, and without options or short positions.

A top-four portfolio without the confidence gate may be reported as an ablation, but it is not another policy to tune.

## 8. Trading-cost assumptions

```text
Base cost:       10 basis points per dollar bought or sold
Stress tests:    20 and 50 basis points
Portfolio cost:  cost_rate * sum(abs(new_weight - old_weight))
```

Results are reported before personal taxes. Any later personal-use analysis must account for the actual account type and applicable tax consequences separately.

## 9. Benchmarks

1. Primary: monthly rebalanced equal weighting of the ten scored ETFs, using the same cost model
2. Passive equity reference: buy-and-hold SPY
3. Diversified reference: 60% SPY / 40% IEF
4. Non-ML competitor: trailing 12-month momentum excluding the most recent month, holding the top four equally

## 10. Time split

- Initial training: 2007–2014
- Expanding walk-forward development: 2015–2022
- Sealed final holdout: January 2023 through the latest completed month in the first immutable data snapshot

Hyperparameters, feature decisions, and portfolio-policy decisions may use only the development period. The sealed holdout is evaluated once after the complete system is frozen.

Mechanical data-quality checks may inspect all dates, but no strategy performance may be calculated on the sealed holdout during development.

## 11. Evaluation

### Primary metric

Net geometric excess return over the equal-weight benchmark on the sealed holdout.

### Secondary metrics

- Spearman rank correlation between scores and next-month returns
- Net annualized return
- Sharpe and Sortino ratios
- Maximum drawdown and recovery time
- Turnover and estimated cost drag
- Brier score and probability-reliability plot
- Performance by calendar year and volatility regime
- Contribution by asset
- Results at base, 2x, and 5x costs
- Results with one additional trading day of execution delay

## 12. Research-success gate

Call the result promising only if:

- Net holdout wealth exceeds the primary benchmark.
- It improves on, or clearly complements, simple momentum.
- The advantage survives doubled costs and delayed execution.
- One asset or one year does not explain the result.
- Risk-adjusted performance and maximum drawdown are not materially worse than the primary benchmark.
- Probability calibration beats a naive constant-probability model.

Failure to pass is a valid research result and means the investment hypothesis was not supported.

## 13. Frozen choices

Once this charter is marked **LOCKED**, do not change these after viewing results:

- Universe
- Target and horizon
- Decision and execution timing
- Feature families
- Model families
- Portfolio policy
- Cost formula
- Benchmarks
- Date splits
- Primary metric

Every experiment and parameter set must be recorded. If the final holdout causes a redesign, it is no longer a holdout; the redesigned system must be evaluated on new forward data.

