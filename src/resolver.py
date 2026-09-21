"""
Inference & Resolver Module for AI Smart Complaint Resolver.
------------------------------------------------------------
Loads the trained machine learning models to:
1. Predict Complaint Category
2. Predict Complaint Urgency
3. Recommend the appropriate civic/municipal Department
4. Generate a concise, actionable summary for dispatchers
"""

import os
import re
import joblib

# Department routing lookup table based on category
DEPARTMENT_DIRECTORY = {
    "Flood": {
        "department": "Disaster Management & Stormwater Division",
        "action": "Dispatch emergency water-pumping teams and flood relief units.",
        "contact_code": "CIVIC-FLD-101",
    },
    "Drainage": {
        "department": "Public Works - Drainage & Sewerage Board",
        "action": "Deploy drainage clearance crew and jetting machines.",
        "contact_code": "CIVIC-DRN-102",
    },
    "Water": {
        "department": "Municipal Water Supply & Treatment Authority",
        "action": "Direct pipeline inspection engineers and emergency water supply tankers.",
        "contact_code": "CIVIC-WTR-103",
    },
    "Waste": {
        "department": "Solid Waste Management & Sanitation Department",
        "action": "Schedule municipal compactor truck and sanitation cleanup crew.",
        "contact_code": "CIVIC-WST-104",
    },
    "Road": {
        "department": "Roads, Bridges & Transportation Authority",
        "action": "Send road repair crew for patching, barricading, or resurfacing.",
        "contact_code": "CIVIC-ROD-105",
    },
    "Electricity": {
        "department": "State Electricity Board / Power Grid Division",
        "action": "Notify electrical substation linesmen and rapid response team.",
        "contact_code": "CIVIC-ELE-106",
    },
    "Infrastructure": {
        "department": "Urban Infrastructure & Civil Engineering Division",
        "action": "Assign structural engineers for safety assessment and restoration.",
        "contact_code": "CIVIC-INF-107",
    },
    "Pollution": {
        "department": "Environmental Protection & Pollution Control Board",
        "action": "Dispatch environmental safety inspectors for air/water quality assessment.",
        "contact_code": "CIVIC-POL-108",
    },
}


def generate_short_summary(complaint_text: str, category: str, urgency: str, department: str) -> str:
    """
    Generates a concise, high-impact operational summary for civic dispatchers.
    
    Extracts key clauses from the citizen's complaint and structures it
    into a standardized 1-2 sentence executive briefing.
    """
    cleaned = complaint_text.strip()
    
    # Split into sentences or clauses
    sentences = [s.strip() for s in re.split(r"[.!?\n]+", cleaned) if s.strip()]
    
    # Choose primary core sentence
    primary_clause = sentences[0] if sentences else cleaned
    
    # Capitalize the first letter if needed
    if primary_clause:
        primary_clause = primary_clause[0].upper() + primary_clause[1:]
        # Remove trailing period if present
        primary_clause = primary_clause.rstrip(".")

    # Generate operational dispatch summary
    if urgency == "Critical":
        summary = (
            f"CRITICAL DISPATCH: {primary_clause}. Immediate priority intervention required "
            f"by {department} to safeguard public safety."
        )
    elif urgency == "High":
        summary = (
            f"HIGH PRIORITY: {primary_clause}. Expedited inspection and corrective measures "
            f"recommended for {department} within 24 hours."
        )
    elif urgency == "Medium":
        summary = (
            f"STANDARD NOTICE: {primary_clause}. Assigned to {department} for scheduled service resolution."
        )
    else:  # Low
        summary = (
            f"ROUTINE LOG: {primary_clause}. Referred to {department} for routine maintenance queue."
        )

    return summary


class ComplaintResolver:
    """
    Resolver class that encapsulates loaded models and provides
    end-to-end complaint analysis.
    """

    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        self.category_model = None
        self.urgency_model = None
        self.load_models()

    def load_models(self):
        """Loads serialized machine learning models from disk."""
        cat_path = os.path.join(self.models_dir, "category_model.joblib")
        urg_path = os.path.join(self.models_dir, "urgency_model.joblib")

        if not os.path.exists(cat_path):
            raise FileNotFoundError(
                f"Category model not found at {cat_path}. Run 'src/train.py' first!"
            )
        if not os.path.exists(urg_path):
            raise FileNotFoundError(
                f"Urgency model not found at {urg_path}. Run 'src/train.py' first!"
            )

        self.category_model = joblib.load(cat_path)
        self.urgency_model = joblib.load(urg_path)

    def analyze(self, message: str) -> dict:
        """
        Analyzes a single English citizen complaint.

        Parameters:
            message (str): The citizen's complaint text.

        Returns:
            dict: Complete prediction containing Category, Urgency, Department,
                  Action plan, Confidence, and Short AI Summary.
        """
        if not message or not message.strip():
            return {
                "error": "Please enter a valid complaint message."
            }

        cleaned_msg = message.strip()

        # 1. Predict Category
        predicted_category = self.category_model.predict([cleaned_msg])[0]
        cat_probs = self.category_model.predict_proba([cleaned_msg])[0]
        cat_conf = max(cat_probs)

        # 2. Predict Urgency
        predicted_urgency = self.urgency_model.predict([cleaned_msg])[0]
        urg_probs = self.urgency_model.predict_proba([cleaned_msg])[0]
        urg_conf = max(urg_probs)

        # 3. Department Routing
        dept_info = DEPARTMENT_DIRECTORY.get(
            predicted_category,
            {
                "department": "General Municipal Public Grievances Cell",
                "action": "Route to civic desk for manual assessment.",
                "contact_code": "CIVIC-GEN-000",
            },
        )
        recommended_department = dept_info["department"]
        recommended_action = dept_info["action"]

        # 4. Generate Short AI-Generated Summary
        summary = generate_short_summary(
            complaint_text=cleaned_msg,
            category=predicted_category,
            urgency=predicted_urgency,
            department=recommended_department,
        )

        return {
            "message": cleaned_msg,
            "category": predicted_category,
            "category_confidence": round(float(cat_conf), 3),
            "urgency": predicted_urgency,
            "urgency_confidence": round(float(urg_conf), 3),
            "department": recommended_department,
            "recommended_action": recommended_action,
            "contact_code": dept_info.get("contact_code", "N/A"),
            "summary": summary,
        }


if __name__ == "__main__":
    # Smoke test inference
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    models_path = os.path.join(base_dir, "models")
    
    try:
        resolver = ComplaintResolver(models_dir=models_path)
        test_case = "Massive sewer main burst flooding the residential street with dirty foul water!"
        result = resolver.analyze(test_case)
        print("\n--- Smoke Test Result ---")
        for k, v in result.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(f"Notice: Models not loaded yet ({e}). Train first with src/train.py.")
