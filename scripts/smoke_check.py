from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    ROOT / "notebooks",
    ROOT / "src",
    ROOT / "data",
    ROOT / "data" / "raw",
    ROOT / "data" / "processed",
    ROOT / "models",
    ROOT / "results",
]

PROCESSED_FILES = [
    ROOT / "data" / "raw" / "fred_macro_monthly_raw.csv",
    ROOT / "data" / "processed" / "aligned_macro_target.csv",
    ROOT / "data" / "processed" / "modeling_table_full.csv",
    ROOT / "data" / "processed" / "feature_registry.json",
    ROOT / "data" / "processed" / "feature_registry_table.csv",
    ROOT / "data" / "processed" / "split_metadata.json",
    ROOT / "data" / "processed" / "target_definition_metadata.json",
]

KEY_RESULT_FILES = [
    ROOT / "results" / "baselines" / "baseline_metrics.json",
    ROOT / "results" / "baselines" / "baseline_table.md",
    ROOT / "results" / "baselines" / "best_baseline_actual_vs_pred.png",
    ROOT / "results" / "lstm" / "metrics.json",
    ROOT / "results" / "lstm" / "learning_curves.png",
    ROOT / "results" / "lstm" / "preds_vs_actuals.png",
    ROOT / "results" / "xgb" / "metrics.json",
    ROOT / "results" / "xgb" / "learning_curve.png",
    ROOT / "results" / "xgb" / "preds_vs_actuals.png",
    ROOT / "results" / "xgb" / "feature_importance.json",
    ROOT / "results" / "xgb" / "feature_importance.png",
    ROOT / "results" / "backtest" / "backtest_metrics.json",
    ROOT / "results" / "backtest" / "backtest_table.md",
    ROOT / "results" / "uncertainty" / "coverage.json",
    ROOT / "results" / "uncertainty" / "uncertainty_plot.png",
    ROOT / "results" / "ablations" / "ablation_results.csv",
    ROOT / "results" / "ablations" / "ablation_summary.md",
    ROOT / "results" / "final" / "final_comparison_table.md",
    ROOT / "results" / "final" / "final_summary.md",
]

EXPECTED_TARGET_NAME = "target_yoy_t_plus_1"


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _check_exists(paths: list[Path], errors: list[str], label: str) -> None:
    for path in paths:
        if not path.exists():
            errors.append(f"[{label}] missing: {_rel(path)}")


def _check_modeling_table_target(errors: list[str]) -> None:
    table_path = ROOT / "data" / "processed" / "modeling_table_full.csv"
    if not table_path.exists():
        return

    with table_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])

    if EXPECTED_TARGET_NAME not in header:
        errors.append(
            "[target] modeling table does not contain expected target column "
            f"{EXPECTED_TARGET_NAME}: {_rel(table_path)}"
        )


def _check_target_definition(errors: list[str]) -> None:
    target_meta_path = ROOT / "data" / "processed" / "target_definition_metadata.json"
    if not target_meta_path.exists():
        return

    meta = _load_json(target_meta_path)
    if meta.get("target_mode") != "yoy":
        errors.append(
            "[target] target_definition_metadata.json expected target_mode='yoy', "
            f"found {meta.get('target_mode')!r}"
        )
    if meta.get("forecast_horizon_months") != 1:
        errors.append(
            "[target] target_definition_metadata.json expected forecast_horizon_months=1, "
            f"found {meta.get('forecast_horizon_months')!r}"
        )
    if meta.get("target_name") != EXPECTED_TARGET_NAME:
        errors.append(
            "[target] target_definition_metadata.json expected target_name="
            f"{EXPECTED_TARGET_NAME!r}, found {meta.get('target_name')!r}"
        )


def _check_metrics_consistency(errors: list[str]) -> None:
    baseline_path = ROOT / "results" / "baselines" / "baseline_metrics.json"
    lstm_path = ROOT / "results" / "lstm" / "metrics.json"
    xgb_path = ROOT / "results" / "xgb" / "metrics.json"
    backtest_path = ROOT / "results" / "backtest" / "backtest_metrics.json"

    baseline = _load_json(baseline_path) if baseline_path.exists() else None
    lstm = _load_json(lstm_path) if lstm_path.exists() else None
    xgb = _load_json(xgb_path) if xgb_path.exists() else None
    backtest = _load_json(backtest_path) if backtest_path.exists() else None

    if baseline and baseline.get("target_name") != EXPECTED_TARGET_NAME:
        errors.append(
            "[metrics] baseline_metrics.json target_name mismatch: "
            f"{baseline.get('target_name')!r}"
        )

    if lstm:
        if lstm.get("target_name") != EXPECTED_TARGET_NAME:
            errors.append(
                "[metrics] lstm/metrics.json target_name mismatch: "
                f"{lstm.get('target_name')!r}"
            )
        target_mode = lstm.get("config", {}).get("target_mode")
        if target_mode not in {"level", "delta"}:
            errors.append(
                "[metrics] lstm/metrics.json missing or invalid config.target_mode; "
                "expected one of {'level', 'delta'}"
            )

    if xgb:
        if xgb.get("target_name") != EXPECTED_TARGET_NAME:
            errors.append(
                "[metrics] xgb/metrics.json target_name mismatch: "
                f"{xgb.get('target_name')!r}"
            )
        target_mode = xgb.get("target_mode")
        if target_mode not in {"level", "delta"}:
            errors.append(
                "[metrics] xgb/metrics.json missing or invalid target_mode; "
                "expected one of {'level', 'delta'}"
            )

        artifacts = xgb.get("artifacts", {})
        expected_json = "results\\xgb\\feature_importance.json"
        expected_png = "results\\xgb\\feature_importance.png"
        if artifacts.get("feature_importance_json") != expected_json:
            errors.append(
                "[naming] xgb artifacts.feature_importance_json expected "
                f"{expected_json!r}, found {artifacts.get('feature_importance_json')!r}"
            )
        if artifacts.get("feature_importance_plot") != expected_png:
            errors.append(
                "[naming] xgb artifacts.feature_importance_plot expected "
                f"{expected_png!r}, found {artifacts.get('feature_importance_plot')!r}"
            )

    if xgb and backtest:
        if backtest.get("target_mode") != xgb.get("target_mode"):
            errors.append(
                "[metrics] backtest target_mode does not match xgb target_mode: "
                f"backtest={backtest.get('target_mode')!r}, xgb={xgb.get('target_mode')!r}"
            )


def _check_final_report_files(errors: list[str]) -> None:
    final_table = ROOT / "results" / "final" / "final_comparison_table.md"
    final_summary = ROOT / "results" / "final" / "final_summary.md"

    if final_table.exists():
        txt = final_table.read_text(encoding="utf-8")
        if "Final Comparison Table" not in txt:
            errors.append("[final] final_comparison_table.md missing expected title")

    if final_summary.exists():
        txt = final_summary.read_text(encoding="utf-8")
        for required in ["Final Winner", "Limitations", "Target-definition sensitivity"]:
            if required not in txt:
                errors.append(f"[final] final_summary.md missing required section/text: {required!r}")


def main() -> int:
    errors: list[str] = []

    _check_exists(REQUIRED_DIRS, errors, label="dirs")
    _check_exists(PROCESSED_FILES, errors, label="processed")
    _check_exists(KEY_RESULT_FILES, errors, label="results")

    _check_modeling_table_target(errors)
    _check_target_definition(errors)
    _check_metrics_consistency(errors)
    _check_final_report_files(errors)

    print("Smoke check root:", ROOT)
    print("Required dirs:", len(REQUIRED_DIRS))
    print("Processed files:", len(PROCESSED_FILES))
    print("Key result files:", len(KEY_RESULT_FILES))

    if errors:
        print("\nSMOKE CHECK: FAIL")
        for err in errors:
            print(" -", err)
        return 1

    print("\nSMOKE CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
