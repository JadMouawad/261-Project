# Project Worklog (For Final Report)

This file tracks implementation steps, fixes, experiments, and outcomes across the notebook workflow.

## How to Use This Log
- Add a new dated entry each time you change data logic, model logic, or evaluation setup.
- Record what changed, why it changed, and what the result was.
- Keep metrics tied to the exact split and target used at that time.

## Current Project Configuration (Latest)
- Target: `target_yoy_t_plus_1`
- Split strategy: `covid_aware`
- Split windows: train/val/test rows = `347 / 24 / 24`
- Date ranges:
  - train end: `2021-11-01`
  - val end: `2023-11-01`
  - test: `2023-12-01` to `2026-01-01`

## Timeline and Changes

### Phase 1 - Project Setup
- Initialized notebook-first scaffold.
- Added core folders: `notebooks/`, `data/raw/`, `data/processed/`, `models/`, `results/`, `src/`.
- Added shared utility module `src/project_utils.py` for deterministic seeds and path handling.
- Added first audit notebook: `notebooks/00_project_overview_and_repo_audit.ipynb`.

### Phase 2 - Data, Features, and Baselines
- Added data ingestion notebook: `notebooks/01_data_ingestion_and_target_definition.ipynb`.
  - FRED load with cache fallback.
  - Explicit target config and metadata save.
  - EDA plots under `results/eda/`.
- Added feature/splits notebook: `notebooks/02_feature_engineering_and_splits.ipynb`.
  - Full engineered feature family implemented.
  - Feature registry (`small` / `full`) saved.
  - Chronological splits + context-window sequence building.
- Added classical baseline notebook: `notebooks/03_classical_baselines.ipynb`.
  - Naive, seasonal naive, ARIMA, Ridge, Lasso.
  - Baseline table and metrics saved under `results/baselines/`.

### Phase 3 - Split Review and Fix
- Issue identified: earlier train split had little/no COVID-period exposure in fitting.
- Fix applied in notebook 02:
  - Added `SPLIT_STRATEGY` with `covid_aware` mode.
  - New default keeps recent months for val/test and includes COVID-era data in train.
- Regenerated downstream outputs after split update.

### Phase 4 - Model Protocol Improvements
- LSTM notebook (`04_lstm_nowcasting.ipynb`):
  - Validation used for epoch selection.
  - Final model refit on `train+val` before test scoring.
- Classical baselines (`03_classical_baselines.ipynb`):
  - Added alpha tuning for Ridge/Lasso.
  - Added linear prediction clipping guardrail to prevent extreme extrapolation in shifted regimes.

### Phase 5 - Focused Tuning
- Ran targeted tuning sweeps for XGBoost and LSTM.
- Key change that improved both models:
  - Predict **delta** (`target - Inflation_prev`) and reconstruct level at inference.
- XGBoost tuned defaults now in notebook 05:
  - `lag_length=24`, `target_mode='delta'`.
- LSTM tuned defaults now in notebook 04:
  - `lag_length=24`, `target_mode='delta'`.
- Tuning artifacts saved:
  - `results/tuning/xgb_tuning_results.csv`
  - `results/tuning/lstm_tuning_results.csv`

## Latest Test Metrics (Current Best Run)
All metrics below are on held-out test (`2023-12-01` to `2026-01-01`).

| Model | MAE | sMAPE | MASE |
| --- | ---: | ---: | ---: |
| XGB (improved, mean_pooled, delta, lag=24) | 0.1693 | 6.0069 | 0.5850 |
| NaiveLast | 0.1787 | 6.3683 | 0.6175 |
| LSTM (improved, delta, lag=24) | 0.1787 | 6.5612 | 0.6176 |
| ARIMA(1,0,0) | 0.3161 | 11.0215 | 1.0922 |
| Lasso(mean_pooled) | 0.8007 | 28.1270 | 2.7669 |
| SeasonalNaive | 0.8453 | 24.1892 | 2.9210 |
| Ridge(mean_pooled) | 1.1356 | 36.6147 | 3.9242 |

## Major Decisions Logged
- Use notebook-first reproducible workflow with saved artifacts in `data/`, `models/`, `results/`.
- Keep deterministic seeds and explicit metadata files for target/splits.
- Keep strict held-out test; tune on validation only.
- Use COVID-aware split because regime coverage in training materially matters.
- Use delta-target formulation for ML models when target level is highly persistent.

## Issues Encountered and Fixes
- `to_markdown` dependency issue (`tabulate` missing):
  - Added robust markdown fallback writer in notebook 03.
- Linear model instability under regime shift:
  - Added clipping guardrail to train+val target range in notebook 03.
- LSTM validation-restore assertion mismatch after delta-target update:
  - Updated restore check to evaluate against fit target (`y_val_fit`).

## Open Items for Final Report
- Add rolling backtest notebook with fully consistent setup and report rolling MAE distribution.
- Add uncertainty and conformal interval notebook using updated best models.
- Add model error slices (high-inflation vs low-inflation months).
- Add ablation table: split strategy, lag length, target mode (`level` vs `delta`).

## Entry Template (Copy/Paste)
```markdown
### New Entry
- Change:
- Why:
- Files touched:
- Verification done:
- Metrics impact:
```


### Phase 6 - Backtesting and Uncertainty
- Added `notebooks/06_backtesting_and_uncertainty.ipynb`.
- Implemented XGBoost walk-forward backtest with expanding windows, per-window chronology checks, and saved JSON/MD summaries.
- Added optional lightweight LSTM rolling section (disabled by default for runtime).
- Implemented LSTM uncertainty with:
  - MC-dropout intervals on test set
  - split-conformal intervals calibrated on validation residuals only
- Saved outputs:
  - `results/backtest/backtest_metrics.json`
  - `results/backtest/backtest_table.md`
  - `results/uncertainty/coverage.json`
  - `results/uncertainty/uncertainty_plot.png`
  - `results/uncertainty/conformal_artifacts.npz`
- Verification completed in notebook:
  - backtest chronology pass
  - empirical coverage recompute pass
  - interval/index alignment pass
