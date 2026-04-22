# Inflation Nowcasting (Notebook-First Course Repo)

This repository is a notebook-first monthly inflation nowcasting project using FRED macro data.

## Project Scope
- Data source: monthly FRED macro series.
- Core models: stacked LSTM and XGBoost baseline.
- Evaluation metrics: MAE, sMAPE, MASE.
- Extras: rolling backtest, MC-dropout uncertainty, split-conformal intervals, and final report artifacts.

## Canonical Target Definition (Important)
The primary project target is:
- `target_yoy_t_plus_1`: next-month CPI YoY inflation.

Notes to avoid ambiguity:
- Notebooks `03` to `06` and the final comparison in `08` evaluate this primary YoY target.
- Notebook `07` includes YoY vs MoM ablations for sensitivity analysis only.
- Model `target_mode` values (`level`/`delta`) indicate model-training representation of the same target signal, not a different macro target definition.

## Folder Layout
```text
.
|-- notebooks/
|-- docs/
|   |-- REPORT.md
|   `-- RESULTS.md
|-- data/
|   |-- raw/
|   `-- processed/
|-- models/
|-- results/
|-- scripts/
|   `-- smoke_check.py
|-- src/
|   `-- project_utils.py
|-- requirements.txt
`-- README.md
```

## Setup
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional API key setup (`.env` recommended):
```bash
cp .env.example .env
# then edit .env and add your real key
```

PowerShell env var also works:
```powershell
$Env:FRED_API_KEY="your_32_char_fred_key"
```

## Final Notebook Order (Run Top-to-Bottom)
1. `notebooks/00_project_overview_and_repo_audit.ipynb`
2. `notebooks/01_data_ingestion_and_target_definition.ipynb`
3. `notebooks/02_feature_engineering_and_splits.ipynb`
4. `notebooks/03_classical_baselines.ipynb`
5. `notebooks/04_lstm_nowcasting.ipynb`
6. `notebooks/05_xgboost_and_tree_models.ipynb`
7. `notebooks/06_backtesting_and_uncertainty.ipynb`
8. `notebooks/07_ablation_and_model_selection.ipynb`
9. `notebooks/08_final_comparison_and_report.ipynb`

Fresh-clone assumption:
- dependencies are installed, and
- either `FRED_API_KEY` is set or cached `data/raw` and `data/processed` files already exist.

## Canonical Artifact Names and Locations
### Data
- `data/raw/fred_macro_monthly_raw.csv`
- `data/processed/aligned_macro_target.csv`
- `data/processed/modeling_table_full.csv`
- `data/processed/feature_registry.json`
- `data/processed/split_metadata.json`
- `data/processed/target_definition_metadata.json`

### Models
- `models/lstm_model.keras`
- `models/lstm_feature_scaler.joblib`

### Results
- Baselines: `results/baselines/baseline_metrics.json`, `baseline_table.md`
- LSTM: `results/lstm/metrics.json`, `learning_curves.png`, `preds_vs_actuals.png`
- XGBoost: `results/xgb/metrics.json`, `learning_curve.png`, `preds_vs_actuals.png`, `feature_importance.json`, `feature_importance.png`
- Backtest: `results/backtest/backtest_metrics.json`, `backtest_table.md`
- Uncertainty: `results/uncertainty/coverage.json`, `uncertainty_plot.png`
- Ablation: `results/ablations/ablation_results.csv`, `ablation_summary.md`
- Final report: `results/final/final_comparison_table.md`, `final_summary.md`

## Verification
Run the compact smoke check:
```bash
python scripts/smoke_check.py
```

What it verifies:
- required folders exist,
- processed data files exist,
- key result files exist,
- target-definition and metric-schema consistency checks pass.
