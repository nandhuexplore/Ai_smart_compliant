"""
Machine Learning Training Pipeline for AI Smart Complaint Resolver.
-------------------------------------------------------------------
Trains two independent text classification models:
1. Category Predictor: Identifies civic problem domain (Flood, Road, Waste, etc.)
2. Urgency Predictor: Identifies urgency level (Low, Medium, High, Critical)

Both models use a scikit-learn Pipeline with TF-IDF Vectorizer and Logistic Regression.
Trained models are saved to the 'models/' directory.
"""

import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

from data_loader import load_complaints_data, inspect_dataset


def build_pipeline() -> Pipeline:
    """
    Constructs a beginner-friendly NLP classification pipeline.
    
    Components:
    1. TfidfVectorizer: Converts English text messages into numerical TF-IDF feature matrices.
       - ngram_range=(1, 2): Captures unigrams ("pothole") and bigrams ("power outage").
       - stop_words='english': Removes generic English words ("the", "is", "at").
       - sublinear_tf=True: Applies sublinear scaling 1 + log(tf) to tame high frequency terms.
    2. LogisticRegression: Linear classifier known for high accuracy and fast inference on text.
       - class_weight='balanced': Gives balanced emphasis across categories.
       - max_iter=1000: Ensures convergence.
    """
    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                stop_words="english",
                sublinear_tf=True,
                min_df=1,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42,
            ),
        ),
    ])


def train_models(dataset_path: str = "dataset/complaints.csv", models_dir: str = "models"):
    """
    Main training routine:
    1. Loads and inspects complaints dataset.
    2. Splits data into training (80%) and testing (20%) sets.
    3. Trains Category classifier and reports accuracy.
    4. Trains Urgency classifier and reports accuracy.
    5. Saves both trained models as joblib files.
    """
    print("=" * 60)
    print("AI SMART COMPLAINT RESOLVER - TRAINING PIPELINE")
    print("=" * 60)

    # 1. Load Data
    print(f"\n[Step 1] Loading dataset from '{dataset_path}'...")
    df = load_complaints_data(dataset_path)
    summary = inspect_dataset(df)
    print(f"Loaded {summary['total_records']} total validated complaint records.")

    # Create models directory if it doesn't exist
    os.makedirs(models_dir, exist_ok=True)

    # -------------------------------------------------------------
    # 2. Train Category Model
    # -------------------------------------------------------------
    print("\n[Step 2] Training Category Classification Model...")
    X = df["Message"]
    y_category = df["Category"]

    X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
        X, y_category, test_size=0.20, random_state=42, stratify=y_category
    )

    category_model = build_pipeline()
    category_model.fit(X_train_cat, y_train_cat)

    # Evaluate Category Model
    cat_preds = category_model.predict(X_test_cat)
    cat_acc = accuracy_score(y_test_cat, cat_preds)
    print(f"Category Model Test Accuracy: {cat_acc * 100:.2f}%\n")
    print("Category Classification Report:")
    print(classification_report(y_test_cat, cat_preds, zero_division=0))

    # Save Category Model
    category_model_path = os.path.join(models_dir, "category_model.joblib")
    joblib.dump(category_model, category_model_path)
    print(f"-> Saved Category Model to: {category_model_path}")

    # -------------------------------------------------------------
    # 3. Train Urgency Model
    # -------------------------------------------------------------
    print("\n[Step 3] Training Urgency Classification Model...")
    y_urgency = df["Urgency"]

    X_train_urg, X_test_urg, y_train_urg, y_test_urg = train_test_split(
        X, y_urgency, test_size=0.20, random_state=42, stratify=y_urgency
    )

    urgency_model = build_pipeline()
    urgency_model.fit(X_train_urg, y_train_urg)

    # Evaluate Urgency Model
    urg_preds = urgency_model.predict(X_test_urg)
    urg_acc = accuracy_score(y_test_urg, urg_preds)
    print(f"Urgency Model Test Accuracy: {urg_acc * 100:.2f}%\n")
    print("Urgency Classification Report:")
    print(classification_report(y_test_urg, urg_preds, zero_division=0))

    # Save Urgency Model
    urgency_model_path = os.path.join(models_dir, "urgency_model.joblib")
    joblib.dump(urgency_model, urgency_model_path)
    print(f"-> Saved Urgency Model to: {urgency_model_path}")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE! Both models successfully built and saved.")
    print("=" * 60)

    return {
        "category_accuracy": cat_acc,
        "urgency_accuracy": urg_acc,
        "category_model_path": category_model_path,
        "urgency_model_path": urgency_model_path,
    }


if __name__ == "__main__":
    # Get paths relative to project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_file = os.path.join(base_dir, "dataset", "complaints.csv")
    output_dir = os.path.join(base_dir, "models")
    
    train_models(dataset_path=data_file, models_dir=output_dir)
