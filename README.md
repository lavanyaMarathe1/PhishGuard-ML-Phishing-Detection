# Phishing Website Detection — ML Mini Project Prototype

## What this prototype contains
- Sample phishing/legitimate URL dataset
- URL feature extraction
- Random Forest model
- Train/test split
- Accuracy, precision, recall, F1-score
- Confusion matrix
- Streamlit web application
- Risk score and simple feature explanations

## Run locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model
```bash
python train_model.py
```

### 3. Start the application
```bash
streamlit run app.py
```

The browser will open the Streamlit application.

## Important
The included dataset is synthetic/sample data for demonstrating the project pipeline.
For the final college project, replace it with a properly sourced real phishing URL dataset
and document its source, preprocessing, limitations, and ethical considerations.
