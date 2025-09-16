# src/train.py
import os
import argparse
from model import train_random_forest, save_model, save_metrics

def main():
    ap = argparse.ArgumentParser(description="Train RandomForest for defect prediction")
    ap.add_argument("--data", default="data/dataset.csv", help="Path to training CSV")
    ap.add_argument("--model-out", default="models/model.pkl", help="Output model pickle")
    ap.add_argument("--metrics-out", default="artifacts/metrics.json", help="Metrics JSON")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.model_out), exist_ok=True)
    os.makedirs(os.path.dirname(args.metrics_out), exist_ok=True)

    print(f"[train] reading data from: {args.data}")
    model, res = train_random_forest(args.data)

    print(f"[train] saving model to: {args.model_out}")
    save_model(model, args.model_out)

    print(f"[train] saving metrics to: {args.metrics_out}")
    save_metrics(res, args.metrics_out)

    print("[train] done")
    print(res.__dict__)

if __name__ == "__main__":
    main()
