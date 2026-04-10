from __future__ import annotations

import os
import random
from pathlib import Path

import numpy as np


def project_root() -> Path:
    """Resolve repository root regardless of notebook working directory."""
    return Path(__file__).resolve().parents[1]


def ensure_project_dirs() -> dict[str, Path]:
    """Create standard output folders and return their paths."""
    root = project_root()
    paths = {
        "root": root,
        "notebooks": root / "notebooks",
        "raw_data": root / "data" / "raw",
        "processed_data": root / "data" / "processed",
        "models": root / "models",
        "results": root / "results",
    }
    for key in ("raw_data", "processed_data", "models", "results"):
        paths[key].mkdir(parents=True, exist_ok=True)
    return paths


def seed_everything(seed: int = 42) -> None:
    """Set deterministic seeds for python, numpy, and TensorFlow if available."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    try:
        import tensorflow as tf

        tf.random.set_seed(seed)
        try:
            tf.config.experimental.enable_op_determinism()
        except Exception:
            pass
    except Exception:
        pass
