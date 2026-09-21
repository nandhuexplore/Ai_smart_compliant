# AI Smart Complaint Resolver

An English-only civic complaint analysis system that automatically categorizes citizen grievances, assesses operational urgency, routes tickets to the appropriate municipal department, and produces an executive dispatch summary.

---

## 📂 Project Structure

```text
d:\ai_compliant\
│
├── dataset/
│   └── complaints.csv             # 160 balanced English community complaints
│
├── models/
│   ├── category_model.joblib      # TF-IDF + LogisticRegression pipeline (Category)
│   └── urgency_model.joblib       # TF-IDF + LogisticRegression pipeline (Urgency)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py             # Data loader, cleaner, and validation
│   ├── train.py                   # Model training and evaluation script
│   └── resolver.py                # Inference, department routing & AI summary generator
│
├── app.py                         # Streamlit web application
├── requirements.txt               # Dependencies
└── README.md                      # Documentation
```

---

## 🏷️ Dataset Specification

- **File**: `dataset/complaints.csv`
- **Columns**: `Message`, `Category`, `Urgency`
- **Categories** (8): `Flood`, `Waste`, `Road`, `Drainage`, `Water`, `Electricity`, `Infrastructure`, `Pollution`
- **Urgency Levels** (4): `Low`, `Medium`, `High`, `Critical`

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Machine Learning Pipeline
```bash
python src/train.py
```
This will:
- Load and validate `dataset/complaints.csv`
- Train the `Category` classifier
- Train the `Urgency` classifier
- Save both models to `models/category_model.joblib` and `models/urgency_model.joblib`

### 3. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open the provided browser URL (default `http://localhost:8501`) to input complaints and view the real-time AI predictions!
