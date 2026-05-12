import pandas as pd
import joblib
import argparse

MODEL_PATH = "models/ids_model.pkl"

def load_model():
    print("Loading model...")
    return joblib.load(MODEL_PATH)

def predict_from_csv(model, csv_path):
    df = pd.read_csv(csv_path)
    predictions = model.predict(df)
    return predictions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IDS Prediction Script")
    parser.add_argument("--input", required=True, help="Path to CSV file with features")
    args = parser.parse_args()

    model = load_model()
    preds = predict_from_csv(model, args.input)

    print("\nPredictions:")
    for i, p in enumerate(preds):
        print(f"Sample {i+1}: {p}")
