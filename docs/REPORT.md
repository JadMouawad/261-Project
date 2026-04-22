# Inflation Nowcasting Report

## 1) Dataset Exploration and Preprocessing

### Dataset used
We use monthly macroeconomic time series from FRED, aligned into one panel and saved locally for reproducibility.

Main variables:
- CPI
- Unemployment
- InterestRate
- M2
- Treasury10Y
- OilPrice
- PPI
- RetailSales
- Sentiment
- Employment
- HousingStarts

Target used for main evaluation:
- `target_yoy_t_plus_1` (next-month CPI year-over-year inflation)

### Preprocessing pipeline
1. Load from FRED when API key is available; otherwise load cached files.
2. Enforce monthly alignment and check for duplicate timestamps.
3. Build inflation targets in leakage-safe way (forecast horizon = 1 month).
4. Engineer macro features (changes, returns, interactions, volatility, seasonal terms, COVID flag).
5. Build chronological train/val/test split using a COVID-aware split policy.

Split configuration used in final runs:
- Train: 347 rows (through 2021-11-01)
- Validation: 24 rows (through 2023-11-01)
- Test: 24 rows (2023-12-01 to 2026-01-01)

### Initial data checks
We inspected:
- date range and missing values
- summary statistics
- target trajectory
- feature correlations
- panel behavior across macro series

Key EDA plots:
- ![Target](results/eda/target_series.png)
- ![Correlation](results/eda/correlation_heatmap.png)
- ![Macro panel](results/eda/macro_panel_zscore.png)

---

## 2) Methodology Followed

### Modeling workflow
The workflow is notebook-first and reproducible:
1. Data ingestion and target definition (`01`)
2. Feature engineering + split logic (`02`)
3. Classical baselines (`03`)
4. LSTM (`04`)
5. XGBoost (`05`)
6. Backtesting + uncertainty (`06`)
7. Ablation and selection (`07`)
8. Final integrated comparison (`08`)

### Leakage controls
- Strict chronological split.
- Validation used for model/tuning decisions.
- Test untouched until final evaluation.
- MASE denominator uses in-sample history only (train+val).
- Conformal calibration uses validation residuals only.

### Reproducibility
- fixed seeds where possible
- cached raw and processed data
- saved model artifacts and metrics under `models/` and `results/`
- smoke-check script verifies required outputs

---

## 3) Selected Models and Justification

We selected a model set that balances interpretability, baseline strength, and sequence learning:

### Classical baselines
- Naive last value
- Seasonal naive
- ARIMA
- Ridge regression
- Lasso regression

Why included:
- establish honest lower/upper baseline range before complex models
- check whether advanced models truly beat simple predictors

### Neural model
- Stacked LSTM

Why included:
- inflation is time-dependent and sequence models can capture temporal interactions

### Tree model
- XGBoost

Why included:
- strong performance on structured engineered features
- robust under small/medium sample sizes
- fast validation-based tuning

### Representation choices tested
For tabular lag windows:
- mean-pooled
- flattened

For ML targets:
- level and delta formulations (`delta` worked better in final selected setup)

---

## 4) Evaluation Metrics and Results

Metrics used:
- MAE (primary)
- sMAPE
- MASE

Held-out evaluation window:
- 2023-12-01 to 2026-01-01

### Final hold-out comparison
| Model | MAE | sMAPE | MASE |
| --- | ---: | ---: | ---: |
| XGBoost (mean_pooled, delta, lag=24) | 0.1584 | 5.7321 | 0.5474 |
| Lasso (mean_pooled, delta, lag=24) | 0.1663 | 5.9219 | 0.5747 |
| LSTM (delta, lag=24) | 0.1787 | 6.5612 | 0.6176 |
| Naive Last | 0.1787 | 6.3683 | 0.6175 |
| ARIMA(1,0,0) | 0.3161 | 11.0215 | 1.0922 |
| Ridge (mean_pooled, delta, lag=24) | 0.3234 | 14.4044 | 1.1177 |
| Seasonal Naive | 0.8453 | 24.1892 | 2.9210 |

### Main result
XGBoost is the final winner by MAE/sMAPE/MASE on shared held-out test.

### Key plots
- ![Holdout metrics](results/final/figures/holdout_metric_comparison.png)
- ![XGB actual vs pred](results/final/figures/xgb_actual_vs_pred.png)
- ![LSTM actual vs pred](results/final/figures/lstm_actual_vs_pred.png)
- ![XGB feature importance](results/final/figures/xgb_feature_importance.png)

### Backtesting and uncertainty
Backtest (XGBoost walk-forward, 25 windows):
- MAE: 0.2946
- sMAPE: 13.3662
- MASE: 1.4372

Uncertainty diagnostics (LSTM):
- MC-dropout coverage: 0.625
- split-conformal coverage: 1.000
- nominal target: 0.900

Plots:
- ![Rolling backtest](results/final/figures/rolling_backtest_summary.png)
- ![Uncertainty intervals](results/final/figures/uncertainty_intervals.png)
- ![Uncertainty coverage](results/final/figures/uncertainty_coverage_summary.png)

### Extra finding: LSTM timing lag
We ran an explicit lag diagnostic and found LSTM often tracks direction with about ~1 month delay.
- see `results/lstm/lag_diagnostic.json`
- see `results/lstm/lag_diagnostic_plot.png`

### Note on `COVID` feature in XGBoost
`COVID` has zero gain in final XGBoost feature importance.
This is expected because:
- the COVID=1 period is short (16 months)
- val/test windows are post-COVID (feature constant at 0 there)
- other macro variables already absorb most regime dynamics

---

## 5) Conclusions

1. The strongest final model is XGBoost with engineered macro features and delta-target training.
2. A tuned linear baseline (Lasso) is surprisingly competitive and close to the winner.
3. LSTM is useful but did not outperform XGBoost on this dataset and split.
4. Time variation remains important: rolling backtest shows regime-dependent error.
5. Uncertainty estimates need recalibration for better practical reliability.

### Final recommendation
For this project submission, use XGBoost as the primary model and present Lasso/LSTM as supporting comparisons.

---

## Deliverables Checklist (Project Requirements)
- Python code (notebooks): Yes
- Report (2-4 pages with plots): Yes (`REPORT.md`)
- Covers dataset exploration and preprocessing: Yes
- Covers methodology followed: Yes
- Covers selected models and justification: Yes
- Covers evaluation metrics and results: Yes
- Covers conclusions: Yes

## Rubric Alignment
- Depth of investigation (30%): multiple model families, backtesting, uncertainty analysis, ablation runs, and lag diagnostics.
- Correctness of approach (30%): chronological split, validation-based selection, leakage-safe target construction, and in-sample-only MASE scaling.
- Clarity of presentation (20%): structured notebook flow, report file, and saved tables/plots under `results/`.
- Understanding of steps involved (20%): explicit explanations for feature design, model choices, split behavior, and failure cases.

## Files for submission
- `notebooks/00` to `notebooks/08`
- `REPORT.md`
- `RESULTS.md`
- `results/final/final_comparison_table.md`
- `results/final/final_summary.md`
