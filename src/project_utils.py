import os
import random
from pathlib import Path

import numpy as np


def project_root():
    return Path(__file__).resolve().parents[1]


def ensure_project_dirs():
    r = project_root()
    p = {}
    p["root"] = r
    p["notebooks"] = r / "notebooks"
    p["raw_data"] = r / "data" / "raw"
    p["processed_data"] = r / "data" / "processed"
    p["models"] = r / "models"
    p["results"] = r / "results"

    for k in ("raw_data","processed_data","models","results"):
        p[k].mkdir(parents=True,exist_ok=True)
    return p


def seed_everything(seed = 42):
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
