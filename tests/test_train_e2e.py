# tests/test_train_e2e.py
import pandas as pd
from src.model import train_random_forest, METRICS


def test_train_end_to_end_small_df():
    # tiny balanced DF made in-memory for determinism
    n = 60
    data = {
        "commit_id": [f"c{i}" for i in range(n)],
        "bugcount": [0] * (n // 2) + [1] * (n - n // 2),
    }
    for m in METRICS:
        data[m] = list(range(n))
    df = pd.DataFrame(data)

    # write to a temporary CSV-like object via pandas to_csv -> string buffer is fine,
    # but train_random_forest expects a path, so we’ll use NamedTemporaryFile pattern:
    import tempfile
    import os
    with tempfile.TemporaryDirectory() as td:
        csv_path = os.path.join(td, "tmp.csv")
        df.to_csv(csv_path, index=False)
        model, res = train_random_forest(csv_path)

    assert hasattr(model, "predict")
    assert 0.0 <= res.accuracy <= 1.0
    assert 0.0 <= res.f1 <= 1.0
