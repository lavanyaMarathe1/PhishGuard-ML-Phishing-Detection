
import os, joblib, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from features import extract_features, FEATURE_NAMES

DATA = "sample_phishing_dataset.csv"
MODEL = "phishing_model.joblib"

df = pd.read_csv(DATA)
X = pd.DataFrame([extract_features(u) for u in df["url"]], columns=FEATURE_NAMES)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200, random_state=42, class_weight="balanced"
)
model.fit(X_train, y_train)

pred = model.predict(X_test)

metrics = {
    "accuracy": accuracy_score(y_test, pred),
    "precision": precision_score(y_test, pred, zero_division=0),
    "recall": recall_score(y_test, pred, zero_division=0),
    "f1": f1_score(y_test, pred, zero_division=0),
    "confusion_matrix": confusion_matrix(y_test, pred).tolist()
}

joblib.dump({
    "model": model,
    "feature_names": FEATURE_NAMES,
    "metrics": metrics
}, MODEL)

print("Model saved:", MODEL)
print("Metrics:", metrics)
