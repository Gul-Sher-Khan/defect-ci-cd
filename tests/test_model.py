import pandas as pd
from src.model import METRICS, _prep


def test_prep_shapes():
    data = {
        "commit_id": ["c1", "c2", "c3", "c4", "c5"],
        "bugcount": [0, 1, 0, 2, 0],
    }
    for m in METRICS:
        data[m] = [1, 2, 3, 4, 5]
    df = pd.DataFrame(data)
    X, y = _prep(df)
    assert X.shape[1] == len(METRICS)
    assert y.sum() == 2
