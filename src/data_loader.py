"""
Data Loader Module for AI Smart Complaint Resolver.
--------------------------------------------------
Handles loading, validating, and preprocessing English community complaints dataset.
"""

import os
import re
import pandas as pd

# Expected categories and urgency levels as defined in project requirements
VALID_CATEGORIES = [
    "Flood",
    "Waste",
    "Road",
    "Drainage",
    "Water",
    "Electricity",
    "Infrastructure",
    "Pollution",
]

VALID_URGENCIES = [
    "Low",
    "Medium",
    "High",
    "Critical",
]


def clean_text(text: str) -> str:
    """
    Cleans raw complaint text for machine learning.
    
    Steps:
    1. Converts text to lowercase.
    2. Strips extra whitespaces.
    3. Retains alphanumeric characters and basic punctuation useful for context.
    """
    if not isinstance(text, str):
        return ""
    
    # Strip leading/trailing whitespaces
    text = text.strip()
    
    # Remove multiple spaces / tabs / newlines
    text = re.sub(r"\s+", " ", text)
    
    return text


def load_complaints_data(csv_path: str = "dataset/complaints.csv") -> pd.DataFrame:
    """
    Loads and validates the complaints CSV file.

    Parameters:
        csv_path (str): Path to the CSV dataset.

    Returns:
        pd.DataFrame: Cleaned and validated dataframe with 'Message', 'Category', 'Urgency'.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at expected path: {csv_path}")

    # Read CSV using pandas
    df = pd.read_csv(csv_path)

    # Validate required columns
    required_cols = ["Message", "Category", "Urgency"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column '{col}' in CSV. Found: {list(df.columns)}")

    # Drop rows with missing values
    df = df.dropna(subset=required_cols).copy()

    # Clean text in Message column
    df["Message"] = df["Message"].apply(clean_text)

    # Standardize Category and Urgency strings (capitalize correctly)
    df["Category"] = df["Category"].str.strip().str.title()
    df["Urgency"] = df["Urgency"].str.strip().str.title()

    # Filter out empty messages
    df = df[df["Message"].str.len() > 0].reset_index(drop=True)

    return df


def inspect_dataset(df: pd.DataFrame) -> dict:
    """
    Inspects and returns key statistics of the dataset for reporting.
    """
    stats = {
        "total_records": len(df),
        "columns": list(df.columns),
        "categories_count": df["Category"].value_counts().to_dict(),
        "urgency_count": df["Urgency"].value_counts().to_dict(),
        "sample_records": df.head(3).to_dict(orient="records"),
    }
    return stats


if __name__ == "__main__":
    # Quick standalone inspection run
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "dataset", "complaints.csv")
    df = load_complaints_data(dataset_path)
    summary = inspect_dataset(df)
    
    print("=== Dataset Inspection Summary ===")
    print(f"Total Complaints: {summary['total_records']}")
    print("\nCategory Distribution:")
    for cat, count in summary["categories_count"].items():
        print(f" - {cat}: {count}")
    print("\nUrgency Distribution:")
    for urg, count in summary["urgency_count"].items():
        print(f" - {urg}: {count}")
