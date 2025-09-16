from __future__ import annotations
import json
import pickle
from dataclasses import dataclass
from typing import Tuple, List, Dict

import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score, accuracy_score, recall_score
)
from sklearn.model_selection import StratifiedShuffleSplit

# Minimal feature set expected in your dataset
METRICS: List[str] = [
    'la',
    'ld',
    'nd',
    'ns',
    'nf',
    'ent',
    'ndev',
    'nuc',
    'age',
    'aexp',
    'asexp',
    'arexp']


def _prep(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    df = df.copy()
    if 'commit_id' not in df.columns or 'bugcount' not in df.columns:
        raise ValueError("CSV must include commit_id and bugcount")
    df['bugcount'] = pd.to_numeric(df['bugcount'], errors='coerce').fillna(0)
    y = (df['bugcount'] > 0).astype(int)
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce') / 3600 / 24
    X = df[METRICS].apply(pd.to_numeric, errors='coerce').fillna(0.0)
    return X, y


def build_rf() -> RandomForestClassifier:
    return RandomForestClassifier(
        bootstrap=False, ccp_alpha=0.0, class_weight=None, criterion='gini',
        max_depth=100, max_features=1, max_leaf_nodes=None, max_samples=None,
        min_impurity_decrease=0.0, min_samples_leaf=1, min_samples_split=2,
        min_weight_fraction_leaf=0.0, n_estimators=1400, n_jobs=None,
        oob_score=False, random_state=42, verbose=0, warm_start=False
    )


@dataclass
class TrainResult:
    auc: float
    f1: float
    precision: float
    recall: float
    accuracy: float


def train_random_forest(csv_path: str):
    df = pd.read_csv(csv_path)
    X, y = _prep(df)

    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    idx_tr, idx_te = next(sss.split(np.zeros(len(y)), y))
    X_tr, y_tr = X.iloc[idx_tr], y.iloc[idx_tr]
    X_te, y_te = X.iloc[idx_te], y.iloc[idx_te]

    X_res, y_res = SMOTEENN(random_state=42).fit_resample(X_tr, y_tr)
    clf = build_rf().fit(X_res, y_res)

    y_pred = clf.predict(X_te)
    res = TrainResult(
        auc=float(roc_auc_score(y_te, y_pred)),
        f1=float(f1_score(y_te, y_pred)),
        precision=float(precision_score(y_te, y_pred)),
        recall=float(recall_score(y_te, y_pred)),
        accuracy=float(accuracy_score(y_te, y_pred)),
    )
    return clf, res


def save_model(model: RandomForestClassifier, path: str) -> None:
    with open(path, "wb") as f:
        pickle.dump(model, f)


def load_model(path: str) -> RandomForestClassifier:
    with open(path, "rb") as f:
        return pickle.load(f)


def save_metrics(res: TrainResult, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(res.__dict__, f, indent=2)
