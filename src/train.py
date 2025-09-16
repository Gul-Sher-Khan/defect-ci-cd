import os
import argparse
from model import train_random_forest, save_model, save_metrics

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/dataset.csv", help="Path to training CSV")
    ap.add_argument("--model-out", default="models/model.pkl", help="Output model pickle")
    ap.add_argument("--metrics-out", default="artifacts/metrics.json", help="Metrics JSON")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.model_out), exist_ok=True)
    os.makedirs(os.path.dirname(args.metrics_out), exist_ok=True)

    model, res = train_random_forest(args.data)
    save_model(model, args.model_out)
    save_metrics(res, args.metrics_out)
    print("Saved:", args.model_out, "and", args.metrics_out)

if __name__ == "__main__":
    main()
