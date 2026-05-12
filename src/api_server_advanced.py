from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np

MODEL_PATH = "models/ids_model_advanced.pkl"

app = FastAPI(title="Advanced Multi-Class IDS API")

# Load enhanced model at startup
model = joblib.load(MODEL_PATH)

# 41 features (NSL-KDD feature 0 to 40)
class TrafficSample(BaseModel):
    features: list

@app.post("/predict")
def predict(sample: TrafficSample):
    # Ensure correct length
    if len(sample.features) != 41:
        return {"error": f"Expected 41 features, but got {len(sample.features)}"}

    df = pd.DataFrame([sample.features])

    # Predict class
    pred_class = int(model.predict(df)[0])

    # Predict probabilities
    probs = model.predict_proba(df)[0]
    prob_dict = {str(i): float(probs[i]) for i in range(len(probs))}

    # Top 3 classes
    top3_idx = np.argsort(probs)[-3:][::-1]
    top3 = {str(int(i)): float(probs[i]) for i in top3_idx}

    return {
        "prediction": pred_class,
        "probabilities": prob_dict,
        "top_3_classes": top3
    }
