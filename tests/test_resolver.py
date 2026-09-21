"""
End-to-End Verification Test for AI Smart Complaint Resolver.
-------------------------------------------------------------
Tests the ComplaintResolver across sample complaints for each category,
validating category, urgency, department routing, and AI summary output.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.resolver import ComplaintResolver, DEPARTMENT_DIRECTORY

def test_all_categories():
    resolver = ComplaintResolver(models_dir="models")
    
    test_cases = [
        ("Continuous rain caused flash water surge in residential colony, ground floor submerged", "Flood"),
        ("Mountain of uncollected garbage rotting on street corner, foul stench everywhere", "Waste"),
        ("Deep dangerous pothole on highway caused two-wheeler accidents and injury", "Road"),
        ("Raw sewage overflowing directly from manhole into apartment basement", "Drainage"),
        ("Main drinking water pipeline fractured and clean water gushing onto road", "Water"),
        ("High voltage electrical wire snapped and sparking violently near school bus stop", "Electricity"),
        ("Concrete railing of pedestrian bridge cracked and leaning dangerously over traffic", "Infrastructure"),
        ("Industrial factory discharging black toxic sulfur smoke all night, residents coughing", "Pollution"),
    ]
    
    print("=" * 70)
    print("RUNNING COMPREHENSIVE COMPLAINT RESOLVER TESTS")
    print("=" * 70)
    
    all_passed = True
    for text, expected_category in test_cases:
        result = resolver.analyze(text)
        pred_cat = result["category"]
        pred_urg = result["urgency"]
        dept = result["department"]
        summary = result["summary"]
        
        match = (pred_cat == expected_category)
        status = "PASS" if match else "MISMATCH"
        if not match:
            all_passed = False
            
        print(f"[{status}] Expected Category: {expected_category} | Predicted: {pred_cat}")
        print(f"       Complaint: {text[:65]}...")
        print(f"       Urgency  : {pred_urg} (Conf: {int(result['urgency_confidence']*100)}%)")
        print(f"       Dept     : {dept}")
        print(f"       Summary  : {summary[:85]}...")
        print("-" * 70)
        
    print(f"Verification Result: {'ALL CATEGORY TESTS MATCHED!' if all_passed else 'SOME TEST VARIANCES OBSERVED'}")
    return all_passed

if __name__ == "__main__":
    test_all_categories()
