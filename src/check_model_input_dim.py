import joblib
import pandas as pd

model = joblib.load("models/ids_model_advanced.pkl")

print("Model expects this many features:", model.n_features_in_)
