import pandas as pd
import numpy as np
import joblib
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.metrics import confusion_matrix

# ============================================================
# 1. Load Data
# ============================================================

DATA_PATH = "data/nsl-kdd/"
train_file = DATA_PATH + "KDDTrain+.txt"
test_file = DATA_PATH + "KDDTest+.txt"

# Use default NSL-KDD numeric split (columns unnamed)
df_train = pd.read_csv(train_file, header=None)
df_test = pd.read_csv(test_file, header=None)

# Last column is attack label (numeric: 0–21)
X_train = df_train.iloc[:, 0:41]
y_train = df_train.iloc[:, 42]


X_test = df_test.iloc[:, 0:41]
y_test = df_test.iloc[:, 42]


# ============================================================
# 2. Preprocessing
# ============================================================

# Categorical feature indices (protocol_type, service, flag)
categorical_idx = [1, 2, 3]

numeric_idx = [i for i in range(41) if i not in categorical_idx]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_idx),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_idx)
])

# ============================================================
# 3. Model Comparison
# ============================================================

models = {
    "RandomForest": RandomForestClassifier(n_estimators=120, max_depth=20, random_state=42),
    "SVM": SVC(kernel="rbf", gamma="scale"),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

results = {}
print("\nTraining models...\n")

for name, model in models.items():
    clf = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    
    start = time.time()
    clf.fit(X_train, y_train)
    duration = time.time() - start
    
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="macro")
    
    results[name] = {"accuracy": acc, "f1": f1, "train_time": duration}

print("\n===== Model Comparison =====")
for m, r in results.items():
    print(f"{m}: Accuracy={r['accuracy']:.4f}, F1={r['f1']:.4f}, TrainTime={r['train_time']:.2f}s")

# ============================================================
# 4. Train Final Model
# ============================================================

final_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(n_estimators=150, max_depth=20, random_state=42))
])

final_model.fit(X_train, y_train)

preds = final_model.predict(X_test)
print("\n===== Final Model Classification Report =====")
print(classification_report(y_test, preds))

# ============================================================
# 5. Feature Importance (after preprocessing)
# ============================================================

rf = final_model.named_steps["model"]
ohe = final_model.named_steps["preprocessor"].named_transformers_["cat"]
ohe_features = ohe.get_feature_names_out()

numeric_features = [f"num_{i}" for i in numeric_idx]
all_features = numeric_features + list(ohe_features)

importances = rf.feature_importances_
feat_df = pd.DataFrame({"feature": all_features, "importance": importances})
feat_df = feat_df.sort_values(by="importance", ascending=False).head(20)

plt.figure(figsize=(10,6))
sns.barplot(data=feat_df, x="importance", y="feature")
plt.title("Top 20 Most Important Features (Numeric NSL-KDD)")
plt.tight_layout()

os.makedirs("figures", exist_ok=True)
plt.savefig("figures/feature_importance_numeric.png")

print("\nSaved feature importance figure: figures/feature_importance_numeric.png")

# ============================================================
# 6. Save Final Model
# ============================================================

os.makedirs("models", exist_ok=True)
joblib.dump(final_model, "models/ids_model_advanced.pkl")

print("\nSaved enhanced model to models/ids_model_advanced.pkl\n")
