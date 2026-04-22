# Results

This is the cleaned final review of what we got from the project.

## 1) Final takeaway
- Best overall model on held-out test: **XGBoost (mean pooled)**
- Best test MAE: **0.1584**
- Strongest classical baseline: **Lasso (mean pooled)** with MAE **0.1663**
- LSTM was solid, but not the best on this dataset

## 2) Main benchmark table
Held-out window: **2023-12-01 to 2026-01-01**

| Model | MAE | sMAPE | MASE | Rank |
| --- | ---: | ---: | ---: | ---: |
| XGBoost (mean_pooled, delta, lag=24) | 0.1584 | 5.7321 | 0.5474 | 1 |
| Lasso (mean_pooled, delta, lag=24) | 0.1663 | 5.9219 | 0.5747 | 2 |
| LSTM (delta, lag=24) | 0.1787 | 6.5612 | 0.6176 | 3 |
| Naive Last | 0.1787 | 6.3683 | 0.6175 | 4 |
| ARIMA(1,0,0) | 0.3161 | 11.0215 | 1.0922 | 5 |
| Ridge (mean_pooled, delta, lag=24) | 0.3234 | 14.4044 | 1.1177 | 6 |
| Seasonal Naive | 0.8453 | 24.1892 | 2.9210 | 7 |

## 3) Important graphs

### Hold-out metric comparison
![Holdout Comparison](results/final/figures/holdout_metric_comparison.png)

### Actual vs predicted (XGBoost)
![XGB Actual vs Pred](results/final/figures/xgb_actual_vs_pred.png)

### Actual vs predicted (LSTM)
![LSTM Actual vs Pred](results/final/figures/lstm_actual_vs_pred.png)

### XGBoost feature importance
![XGB Feature Importance](results/final/figures/xgb_feature_importance.png)

### Rolling backtest stability
![Rolling Backtest](results/final/figures/rolling_backtest_summary.png)

### Uncertainty intervals (LSTM)
![Uncertainty Intervals](results/final/figures/uncertainty_intervals.png)

## 4) Which features mattered most (XGBoost)
Top features by gain from `results/xgb/feature_importance.json`:

| Feature | Gain |
| --- | ---: |
| Oil_ret_sq | 2.3577 |
| T10Y | 2.2083 |
| Infl_ema | 2.1869 |
| Rate_d_sq | 1.8711 |
| PPI_yoy_sq | 1.8398 |
| PPI_yoy | 1.7888 |
| Housing_d | 1.7237 |
| Inflation_prev | 1.5793 |
| Unemp_d_sq | 1.5135 |
| Oil_ret | 1.1803 |

Interpretation in plain words:
- Energy and producer-price dynamics are very important (`Oil_ret_sq`, `PPI_yoy`, `PPI_yoy_sq`)
- Interest-rate / yield-side info matters (`Rate_d_sq`, `T10Y`)
- Inflation memory still matters (`Infl_ema`, `Inflation_prev`)

## 5) Full engineered feature families used
Modeling table includes these groups:
- **Labor:** `Unemp_d`, `Employment_d`, `Unemp_d_sq`
- **Rates / policy:** `Rate_d`, `Rate_d_sq`, `T10Y`, `Rate_Unemp`
- **Commodities / prices:** `Oil_ret`, `Oil_ret_sq`, `PPI_yoy`, `PPI_yoy_sq`, `Oil_PPI`
- **Money / demand / sentiment:** `M2_yoy`, `Retail_yoy`, `Sentiment`
- **Housing:** `Housing_d`
- **Inflation memory / volatility:** `Infl_ema`, `Infl_vol6`, `Inflation_prev`
- **Calendar / regime:** `MoY_sin`, `MoY_cos`, `COVID`

### Note on `COVID` feature importance
`COVID` has zero gain in the final XGBoost model, and this is expected in our setup.

Why:
- the `COVID=1` period is short (16 months: 2020-03 to 2021-06)
- validation and test windows are post-COVID in this split, so `COVID` is always 0 there
- XGBoost selected splits that generalize on validation, and `COVID` does not add signal in those windows
- pandemic dynamics are already indirectly captured by other macro features (rates, oil, labor, inflation-memory features)

## 6) Robustness checks
- Rolling walk-forward (XGBoost):
  - MAE: **0.2946**
  - sMAPE: **13.3662**
  - MASE: **1.4372**
- Meaning: performance changes across time windows, especially around regime shifts.

## 7) Uncertainty check
Nominal target coverage was 0.90.

- MC-dropout:
  - coverage: **0.625**
  - avg interval width: **0.4416**
- Split-conformal:
  - coverage: **1.000**
  - avg interval width: **1.8473**

So one method is too narrow, the other is too wide in this run.

## 8) What got better after tuning
- XGBoost improved from around **0.1611** MAE to **0.1584** MAE.
- Lasso became competitive after delta-target fitting + stable guardrails.
- Final winner stayed XGBoost.

## 9) Final honest conclusion
For this dataset and split setup, **XGBoost is the safest top model**.

LSTM is still useful for sequence comparison, but with this monthly sample size and feature set,
classical + tree methods stayed more reliable.

## 10) Where all this came from
- `results/final/final_comparison_table.md`
- `results/final/final_summary.md`
- `results/xgb/metrics.json`
- `results/xgb/feature_importance.json`
- `results/lstm/metrics.json`
- `results/backtest/backtest_metrics.json`
- `results/uncertainty/coverage.json`
