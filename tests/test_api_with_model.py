# tests/test_api_with_model.py
import os
import tempfile
import pandas as pd
from src.app import app
from src.model import METRICS, save_model, build_rf

def test_predict_with_temp_model(monkeypatch):
    # train a tiny RF on dummy features only for this test
    X = pd.DataFrame([{m: i for m in METRICS} for i in range(10)])
    y = [0]*5 + [1]*5
    clf = build_rf().fit(X, y)

    with tempfile.TemporaryDirectory() as td:
        model_path = os.path.join(td, "m.pkl")
        save_model(clf, model_path)
        monkeypatch.setenv("MODEL_PATH", model_path)

        client = app.test_client()
        inst = {m: 1 for m in METRICS}
        r = client.post("/predict", json={"instances":[inst, inst]})
        assert r.status_code == 200
        data = r.get_json()
        assert "predictions" in data
        assert isinstance(data["predictions"], list)
        assert len(data["predictions"]) == 2
