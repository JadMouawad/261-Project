# Inflation Nowcasting (Course Project)

This repository is a notebook-first class project for monthly inflation nowcasting.

## Project goal
Build a reproducible monthly inflation nowcasting pipeline using FRED macro series, with:
- robust data and feature engineering,
- sequence and tabular baselines (stacked LSTM and XGBoost),
- transparent evaluation (MAE, sMAPE, MASE),
- uncertainty and interval estimates,
- clean artifacts under `data/`, `models/`, and `results/`.

## Folder layout

```text
.
|-- notebooks/
|   `-- 00_project_overview_and_repo_audit.ipynb
|-- data/
|   |-- raw/
|   `-- processed/
|-- models/
|-- results/
|-- src/
|   `-- project_utils.py
|-- requirements.txt
`-- README.md
```

## Notebook-first workflow
1. Open `notebooks/00_project_overview_and_repo_audit.ipynb`.
2. Run cells top-to-bottom.
3. Continue with later numbered notebooks as they are added.

Each notebook is designed to run on a fresh clone after dependency installation, assuming either:
- `FRED_API_KEY` is set, or
- cached local data already exists under `data/raw/` and `data/processed/`.

## Setup

```bash
python -m venv .venv
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Optional API key setup:

```powershell
$Env:FRED_API_KEY="your_32_char_fred_key"
```

## Reproducibility conventions
- Fixed seeds are used in notebooks/utilities where possible.
- Raw downloads and processed datasets are cached locally.
- Model binaries go to `models/`.
- Tables, metrics, and plots go to `results/`.
- Shared helpers live in `src/project_utils.py`.

## Planned notebook sequence
- `00_project_overview_and_repo_audit.ipynb`: project scope, repo audit, target-definition decision.
- `01_data_ingestion_and_caching.ipynb`: FRED pull plus local cache strategy.
- `02_feature_engineering_and_targets.ipynb`: engineered features plus configurable target definition.
- `03_splits_and_sequence_building.ipynb`: 70/15/15 split, context windows, deterministic dataset objects.
- `04_lstm_baseline.ipynb`: stacked LSTM training and evaluation.
- `05_xgboost_baseline.ipynb`: tabular baseline and comparison.
- `06_backtesting_and_uncertainty.ipynb`: rolling backtest, MC-dropout, conformal intervals.
- `07_results_summary.ipynb`: model comparison table and final visuals.
