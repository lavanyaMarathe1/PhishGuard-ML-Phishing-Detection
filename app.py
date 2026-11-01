
import os
import joblib
import pandas as pd
import streamlit as st
from features import extract_features, FEATURE_NAMES

st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🔐",
    layout="wide"
)

MODEL_FILE = "phishing_model.joblib"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE)

bundle = load_model()
model = bundle["model"]
metrics = bundle["metrics"]

st.title("🔐 Phishing Website Detector")
st.caption("Machine Learning Mini Project — Sample Prototype")

st.markdown(
    "Enter a website URL below. The application extracts URL-based features "
    "and uses a Random Forest model to estimate whether the URL is legitimate or phishing."
)

url = st.text_input(
    "🌐 Enter Website URL",
    placeholder="https://example.com"
)

col1, col2 = st.columns([1, 1])

with col1:
    check = st.button("🔍 Check Website", use_container_width=True)

if check:
    if not url.strip():
        st.warning("Please enter a URL.")
    else:
        x = pd.DataFrame([extract_features(url)], columns=FEATURE_NAMES)
        probability = float(model.predict_proba(x)[0][1])
        prediction = int(model.predict(x)[0])

        # Risk score shown as probability of phishing
        risk = probability * 100

        st.divider()

        if prediction == 1:
            st.error("🔴 PHISHING WEBSITE")
        else:
            st.success("🟢 LEGITIMATE WEBSITE")

        a, b, c = st.columns(3)
        a.metric("Phishing Risk", f"{risk:.1f}%")
        b.metric("Model Confidence", f"{max(probability, 1-probability)*100:.1f}%")
        c.metric("URL Length", str(len(url)))

        st.progress(min(1.0, probability))

        st.subheader("🧠 URL Feature Analysis")

        checks = []
        if len(url) > 75:
            checks.append("Long URL")
        if url.count("@") > 0:
            checks.append("Contains @ symbol")
        if x.loc[0, "has_ip"] == 1:
            checks.append("Uses an IP address")
        if x.loc[0, "num_subdomains"] >= 3:
            checks.append("Many subdomains")
        if x.loc[0, "has_https"] == 0:
            checks.append("No HTTPS")
        if x.loc[0, "suspicious_word_count"] > 0:
            checks.append("Contains security/login-related keywords")
        if x.loc[0, "has_shortener"] == 1:
            checks.append("Uses a URL shortener")

        if checks:
            for item in checks:
                st.write("⚠️", item)
        else:
            st.write("✅ No major URL-level warning indicators detected.")

        with st.expander("View extracted features"):
            st.dataframe(x.T.rename(columns={0: "Value"}), use_container_width=True)

st.divider()

st.subheader("📊 Model Performance")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Accuracy", f"{metrics['accuracy']*100:.2f}%")
m2.metric("Precision", f"{metrics['precision']*100:.2f}%")
m3.metric("Recall", f"{metrics['recall']*100:.2f}%")
m4.metric("F1 Score", f"{metrics['f1']*100:.2f}%")

st.subheader("Confusion Matrix")
cm = pd.DataFrame(
    metrics["confusion_matrix"],
    index=["Actual Legitimate", "Actual Phishing"],
    columns=["Predicted Legitimate", "Predicted Phishing"]
)
st.dataframe(cm, use_container_width=True)

st.info(
    "⚠️ Educational prototype: this model analyzes URL-level patterns only. "
    "It should not be used as a real cybersecurity protection system."
)
