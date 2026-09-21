"""
AI Smart Complaint Resolver - Streamlit Web Application
-------------------------------------------------------
An English-only civic complaint analysis dashboard.
Takes user complaint text, predicts Category & Urgency using trained ML models,
routes to the appropriate municipal Department, and displays a short AI dispatch summary.
"""

import os
import streamlit as st
from src.resolver import ComplaintResolver, DEPARTMENT_DIRECTORY
from src.data_loader import VALID_CATEGORIES, VALID_URGENCIES

# Page configuration
st.set_page_config(
    page_title="AI Smart Complaint Resolver",
    page_icon="🏛️",
    layout="wide",
)

# Custom styling for high quality visual appeal
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .result-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .badge-critical {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-high {
        background-color: #FFEDD5;
        color: #C2410C;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-medium {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-low {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
    }
    .category-badge {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_resolver():
    """Caches the ML resolver so models are loaded only once."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    return ComplaintResolver(models_dir=models_dir)


def render_urgency_badge(urgency: str):
    """Renders HTML badge styled by Urgency level."""
    urgency_lower = urgency.lower()
    if urgency_lower == "critical":
        return f'<span class="badge-critical">🚨 CRITICAL</span>'
    elif urgency_lower == "high":
        return f'<span class="badge-high">⚠️ HIGH</span>'
    elif urgency_lower == "medium":
        return f'<span class="badge-medium">⚡ MEDIUM</span>'
    else:
        return f'<span class="badge-low">🟢 LOW</span>'


def main():
    # Header Section
    st.markdown('<div class="main-title">🏛️ AI Smart Complaint Resolver</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">English Community Complaint Analysis & Civic Routing System</div>',
        unsafe_allow_html=True,
    )

    # Check if models exist
    try:
        resolver = get_resolver()
    except Exception as err:
        st.error(
            f"**Models Not Found!** Please train the machine learning models first by running `python src/train.py`.\n\nError: {err}"
        )
        st.stop()

    # Sidebar: Project Guide & Sample Complaints
    with st.sidebar:
        st.header("📋 Quick Samples")
        st.caption("Click any sample below to load into the text input:")

        samples = [
            ("⚡ Live Electric Wire", "High-voltage 11kV electrical transformer exploded and live sparking wires whipped onto wet road near crowded bus stop!"),
            ("🚰 Water Pipeline Burst", "Main potable water pipeline fractured on 8th Street, clean drinking water gushing onto road."),
            ("🗑️ Rotten Garbage Pile", "Huge heap of rotten municipal waste accumulating at street corner for a week, terrible stench and stray dogs."),
            ("🕳️ Dangerous Road Crater", "Deep dangerous pothole on the middle of Main Arterial Road, several bikes have crashed and riders injured."),
            ("🌊 Flash Flood Warning", "Severe flash flood submerged ground floor houses completely, elderly people stranded on roofs, immediate rescue needed!"),
            ("🏭 Factory Chemical Odor", "Commercial electroplating workshop dumping untreated acidic runoff directly into open public stormwater canal."),
        ]

        # Initialize session state for input
        if "complaint_input" not in st.session_state:
            st.session_state.complaint_input = ""

        for label, text in samples:
            if st.button(label, use_container_width=True):
                st.session_state.complaint_input = text

        st.divider()
        st.subheader("📌 Supported Categories")
        st.markdown(", ".join(f"`{c}`" for c in VALID_CATEGORIES))

        st.subheader("🎯 Urgency Levels")
        st.markdown(", ".join(f"`{u}`" for u in VALID_URGENCIES))

    # Main Input Form
    st.markdown("### ✍️ Enter Community Complaint")
    complaint_text = st.text_area(
        label="Complaint Text (English only):",
        value=st.session_state.complaint_input,
        placeholder="Type or paste the citizen's complaint here in English (e.g., 'A deep pothole on Main Street is causing traffic accidents...').",
        height=130,
    )

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        analyze_clicked = st.button("🔍 Analyze Complaint", type="primary", use_container_width=True)

    # Results Section
    if analyze_clicked or (complaint_text and complaint_text == st.session_state.complaint_input and st.session_state.complaint_input != ""):
        if not complaint_text.strip():
            st.warning("⚠️ Please enter a complaint description before analyzing.")
        else:
            with st.spinner("Analyzing complaint with AI models..."):
                result = resolver.analyze(complaint_text)

            if "error" in result:
                st.error(result["error"])
            else:
                st.markdown("---")
                st.markdown("### 📊 AI Analysis Results")

                # Metrics Row
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Predicted Category**")
                    category_name = result["category"]
                    conf = int(result["category_confidence"] * 100)
                    st.markdown(
                        f'<div style="margin-top: 6px;"><span class="category-badge">{category_name}</span> '
                        f'<span style="font-size:0.85rem; color:#6B7280;">({conf}% match)</span></div>',
                        unsafe_allow_html=True,
                    )

                with col2:
                    st.markdown("**Predicted Urgency**")
                    urgency_name = result["urgency"]
                    urg_conf = int(result["urgency_confidence"] * 100)
                    badge_html = render_urgency_badge(urgency_name)
                    st.markdown(
                        f'<div style="margin-top: 6px;">{badge_html} '
                        f'<span style="font-size:0.85rem; color:#6B7280;">({urg_conf}% confidence)</span></div>',
                        unsafe_allow_html=True,
                    )

                with col3:
                    st.markdown("**Routing Department Code**")
                    st.code(result.get("contact_code", "CIVIC-GEN-000"), language="text")

                st.markdown("<br>", unsafe_allow_html=True)

                # Department & Summary Cards
                dept_col, summary_col = st.columns(2)

                with dept_col:
                    st.markdown("#### 🏢 Recommended Department")
                    st.info(f"**{result['department']}**")
                    st.markdown(f"**Recommended Action:** {result['recommended_action']}")

                with summary_col:
                    st.markdown("#### 📝 Short AI-Generated Summary")
                    st.success(result["summary"])

    # Footer
    st.markdown("---")
    st.caption("AI Smart Complaint Resolver | English-only Community Grievance Analysis Pipeline")


if __name__ == "__main__":
    main()
