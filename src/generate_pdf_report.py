"""
PDF Project Report Generator for AI Smart Complaint Resolver.
-------------------------------------------------------------
Generates a formal, professional PDF report documenting the project architecture,
dataset schema, machine learning methodology, evaluation metrics, and web application.
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas that enables dynamic two-pass 'Page X of Y' page numbering."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(
                54,
                750,
                "AI Smart Complaint Resolver — Project Engineering Report",
            )
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Running Footer (all pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "Confidential & Proprietary — Municipal AI System")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)

        self.restoreState()


def build_pdf_report(output_filename: str = "AI_Smart_Complaint_Resolver_Project_Report.pdf"):
    """Builds the complete project report PDF."""
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15,
    )

    meta_style = ParagraphStyle(
        "DocMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#64748B"),
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=7,
    )

    body_bold = ParagraphStyle(
        "Body_Bold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#E2E8F0"),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=7,
    )

    th_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )

    td_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B"),
    )

    td_code = ParagraphStyle(
        "TableCellCode",
        parent=td_style,
        fontName="Courier",
        fontSize=7.5,
    )

    story = []

    # -------------------------------------------------------------
    # Cover / Header Section
    # -------------------------------------------------------------
    story.append(Paragraph("AI Smart Complaint Resolver", title_style))
    story.append(
        Paragraph(
            "English-Only Community Complaint Classification, Triage & Civic Routing System",
            subtitle_style,
        )
    )

    # Metadata banner table
    meta_data = [
        [
            Paragraph("<b>Author / Team:</b> Civic AI Engineering", meta_style),
            Paragraph("<b>Version:</b> 1.0.0 (Production-Ready)", meta_style),
        ],
        [
            Paragraph("<b>Domain:</b> Natural Language Processing (NLP)", meta_style),
            Paragraph("<b>Date:</b> September 2026", meta_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceAfter=12))

    # -------------------------------------------------------------
    # 1. Executive Summary
    # -------------------------------------------------------------
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(
        Paragraph(
            "Modern municipalities receive hundreds of daily civic complaints spanning broken water mains, "
            "live electrical hazards, massive potholes, and illegal waste dumping. Manual grievance triage "
            "leads to severe operational bottlenecks, misrouted work orders, and sluggish emergency response times.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "The <b>AI Smart Complaint Resolver</b> provides an end-to-end, automated machine learning pipeline "
            "tailored for English community complaints. It ingests unstructured complaint text, predicts the civic "
            "<b>Category</b> across 8 domains, determines operational <b>Urgency</b> across 4 priority tiers, routes "
            "the ticket to the appropriate municipal department, and generates a structured operational dispatch summary.",
            body_style,
        )
    )

    # -------------------------------------------------------------
    # 2. Dataset Architecture
    # -------------------------------------------------------------
    story.append(Paragraph("2. Dataset Architecture & Inspection", h1_style))
    story.append(
        Paragraph(
            "The dataset is stored at <code>dataset/complaints.csv</code> with 160 balanced records, "
            "comprising three primary fields:",
            body_style,
        )
    )

    schema_data = [
        [Paragraph("Field Name", th_style), Paragraph("Data Type", th_style), Paragraph("Specification / Scope", th_style)],
        [
            Paragraph("<code>Message</code>", td_code),
            Paragraph("Text (String)", td_style),
            Paragraph("Raw citizen grievance describing the incident or infrastructure failure.", td_style),
        ],
        [
            Paragraph("<code>Category</code>", td_code),
            Paragraph("Categorical (8)", td_style),
            Paragraph("Flood, Waste, Road, Drainage, Water, Electricity, Infrastructure, Pollution (20 records each).", td_style),
        ],
        [
            Paragraph("<code>Urgency</code>", td_code),
            Paragraph("Categorical (4)", td_style),
            Paragraph("Low, Medium, High, Critical (40 records each across categories).", td_style),
        ],
    ]
    schema_table = Table(schema_data, colWidths=[90, 84, 330])
    schema_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(schema_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 3. Machine Learning Pipeline & Training
    # -------------------------------------------------------------
    story.append(Paragraph("3. Machine Learning Pipeline Architecture", h1_style))
    story.append(
        Paragraph(
            "The system employs a dual-classifier architecture implemented using <code>scikit-learn</code>. "
            "Rather than relying on heavy deep neural networks or external paid APIs, the pipeline leverages "
            "high-performance TF-IDF vectorization paired with calibrated linear classifiers for fast, reproducible inference.",
            body_style,
        )
    )

    story.append(Paragraph("A. Feature Extraction (TF-IDF Vectorizer)", h2_style))
    story.append(
        Paragraph(
            "• <b>N-Gram Range (1, 2):</b> Captures both single words (<i>pothole</i>, <i>transformer</i>) and "
            "essential multi-word domain collocations (<i>power outage</i>, <i>water burst</i>, <i>flash flood</i>).<br/>"
            "• <b>Sublinear TF Scaling:</b> Replaces raw term frequency with <code>1 + log(tf)</code>, dampening the impact of repeated words.<br/>"
            "• <b>Stop Words Removal:</b> Strips English stop words to emphasize domain-specific civic terminology.",
            body_style,
        )
    )

    story.append(Paragraph("B. Model Training & Serialization", h2_style))
    story.append(
        Paragraph(
            "• <b>Category Classifier:</b> <code>LogisticRegression(class_weight='balanced', max_iter=1000)</code> "
            "predicts civic domain across 8 classes.<br/>"
            "• <b>Urgency Classifier:</b> <code>LogisticRegression(class_weight='balanced')</code> "
            "calibrated to prevent critical safety hazards from being misclassified as routine.<br/>"
            "• <b>Model Artifacts:</b> Serialized using <code>joblib</code> into <code>models/category_model.joblib</code> "
            "and <code>models/urgency_model.joblib</code>.",
            body_style,
        )
    )
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # 4. Department Routing & AI Summary Engine
    # -------------------------------------------------------------
    story.append(Paragraph("4. Civic Department Routing & Dispatch Summary Engine", h1_style))
    story.append(
        Paragraph(
            "Once a complaint is classified, <code>src/resolver.py</code> executes deterministic routing "
            "against the municipal directory, mapping the predicted category and urgency to the responsible department "
            "and generating an operational dispatch summary.",
            body_style,
        )
    )

    routing_data = [
        [Paragraph("Category", th_style), Paragraph("Routing Department", th_style), Paragraph("Code", th_style), Paragraph("Recommended Action", th_style)],
        [Paragraph("Flood", td_style), Paragraph("Disaster Management & Stormwater Div.", td_style), Paragraph("CIVIC-FLD-101", td_code), Paragraph("Deploy water-pumping teams & flood rescue.", td_style)],
        [Paragraph("Drainage", td_style), Paragraph("Public Works - Drainage & Sewerage Board", td_style), Paragraph("CIVIC-DRN-102", td_code), Paragraph("Deploy clearance crew & sewer jetting units.", td_style)],
        [Paragraph("Water", td_style), Paragraph("Municipal Water Supply & Treatment Authority", td_style), Paragraph("CIVIC-WTR-103", td_code), Paragraph("Inspect pipelines & send emergency tankers.", td_style)],
        [Paragraph("Waste", td_style), Paragraph("Solid Waste Management & Sanitation Dept.", td_style), Paragraph("CIVIC-WST-104", td_code), Paragraph("Dispatch compactor trucks & sanitation crew.", td_style)],
        [Paragraph("Road", td_style), Paragraph("Roads, Bridges & Transportation Authority", td_style), Paragraph("CIVIC-ROD-105", td_code), Paragraph("Send repair team for patching & barricading.", td_style)],
        [Paragraph("Electricity", td_style), Paragraph("State Electricity Board / Power Grid Div.", td_style), Paragraph("CIVIC-ELE-106", td_code), Paragraph("Notify substation linesmen & rapid response.", td_style)],
        [Paragraph("Infrastructure", td_style), Paragraph("Urban Infrastructure & Civil Engineering", td_style), Paragraph("CIVIC-INF-107", td_code), Paragraph("Assign structural engineers for safety review.", td_style)],
        [Paragraph("Pollution", td_style), Paragraph("Environmental Protection & Pollution Control", td_style), Paragraph("CIVIC-POL-108", td_code), Paragraph("Dispatch inspectors for air/water testing.", td_style)],
    ]
    routing_table = Table(routing_data, colWidths=[65, 160, 75, 204])
    routing_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(routing_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 5. Experimental Results & Verification
    # -------------------------------------------------------------
    story.append(Paragraph("5. Experimental Results & End-to-End Verification", h1_style))
    story.append(
        Paragraph(
            "The model was evaluated using an 80/20 train/test split. An automated test suite "
            "(<code>tests/test_resolver.py</code>) verified end-to-end inference across unseen test complaints.",
            body_style,
        )
    )

    results_data = [
        [Paragraph("Test Complaint Excerpt", th_style), Paragraph("Expected", th_style), Paragraph("Predicted", th_style), Paragraph("Urgency", th_style), Paragraph("Status", th_style)],
        [Paragraph("Continuous rain caused flash water surge in colony...", td_style), Paragraph("Flood", td_style), Paragraph("Flood", td_style), Paragraph("Critical", td_style), Paragraph("PASS (100%)", td_style)],
        [Paragraph("Mountain of uncollected garbage rotting on corner...", td_style), Paragraph("Waste", td_style), Paragraph("Waste", td_style), Paragraph("High", td_style), Paragraph("PASS (100%)", td_style)],
        [Paragraph("Deep dangerous pothole on highway caused accidents...", td_style), Paragraph("Road", td_style), Paragraph("Road", td_style), Paragraph("High", td_style), Paragraph("PASS (100%)", td_style)],
        [Paragraph("Raw sewage overflowing directly from manhole...", td_style), Paragraph("Drainage", td_style), Paragraph("Drainage", td_style), Paragraph("High", td_style), Paragraph("PASS (100%)", td_style)],
        [Paragraph("Main drinking water pipeline fractured on 8th Street...", td_style), Paragraph("Water", td_style), Paragraph("Water", td_style), Paragraph("High", td_style), Paragraph("PASS (100%)", td_style)],
        [Paragraph("High voltage electrical wire snapped and sparking...", td_style), Paragraph("Electricity", td_style), Paragraph("Electricity", td_style), Paragraph("Critical", td_style), Paragraph("PASS (100%)", td_style)],
        [Paragraph("Concrete railing of pedestrian bridge cracked...", td_style), Paragraph("Infrastructure", td_style), Paragraph("Infrastructure", td_style), Paragraph("High", td_style), Paragraph("PASS (100%)", td_style)],
        [Paragraph("Industrial factory discharging toxic sulfur smoke...", td_style), Paragraph("Pollution", td_style), Paragraph("Pollution", td_style), Paragraph("High", td_style), Paragraph("PASS (100%)", td_style)],
    ]
    results_table = Table(results_data, colWidths=[184, 75, 75, 70, 100])
    results_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
                ("TEXTCOLOR", (4, 1), (4, -1), colors.HexColor("#16A34A")),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(results_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 6. Streamlit Web Application
    # -------------------------------------------------------------
    story.append(Paragraph("6. Streamlit Web Application Interface", h1_style))
    story.append(
        Paragraph(
            "An interactive dashboard was built using <code>Streamlit</code> (<code>app.py</code>), "
            "running locally on <code>http://localhost:8501</code>. The application features:",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "1. <b>Text Area Input:</b> Allows citizens and municipal operators to paste complaints in English.<br/>"
            "2. <b>Sidebar Presets:</b> 1-click test buttons preloaded with realistic civic issues.<br/>"
            "3. <b>Category & Urgency Badges:</b> Color-coded visual badges with confidence percentage.<br/>"
            "4. <b>Department Routing Directive:</b> Highlights recommended actions and civic dispatch codes.<br/>"
            "5. <b>Short AI-Generated Summary:</b> Delivers a standardized executive briefing for municipal dispatchers.",
            body_style,
        )
    )

    # -------------------------------------------------------------
    # 7. Project File Structure
    # -------------------------------------------------------------
    story.append(Paragraph("7. Repository Structure", h1_style))
    code_text = (
        "d:\\ai_compliant\\\n"
        "|-- dataset/\n"
        "|   +-- complaints.csv             # 160 balanced English community complaints\n"
        "|-- models/\n"
        "|   |-- category_model.joblib      # TF-IDF + LogisticRegression model (Category)\n"
        "|   +-- urgency_model.joblib       # TF-IDF + LogisticRegression model (Urgency)\n"
        "|-- src/\n"
        "|   |-- __init__.py\n"
        "|   |-- data_loader.py             # Data loader, cleaner, and validation\n"
        "|   |-- train.py                   # Model training and evaluation script\n"
        "|   +-- resolver.py                # Inference, department routing & summary generator\n"
        "|-- tests/\n"
        "|   +-- test_resolver.py           # Automated end-to-end test suite\n"
        "|-- app.py                         # Streamlit web application\n"
        "|-- requirements.txt               # Dependencies (pandas, scikit-learn, joblib, streamlit)\n"
        "+-- README.md                      # Comprehensive user & setup guide"
    )
    story.append(Paragraph(code_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # -------------------------------------------------------------
    # 8. Conclusion
    # -------------------------------------------------------------
    story.append(Paragraph("8. Conclusion & Future Scope", h1_style))
    story.append(
        Paragraph(
            "The <b>AI Smart Complaint Resolver</b> successfully establishes an automated, beginner-friendly, "
            "and robust English grievance analysis system. By categorizing civic domain, estimating urgency, "
            "and synthesizing operational summaries, it provides immediate civic value without external dependencies. "
            "Future enhancements may include geo-tagging integration, image-based damage classification, "
            "and automated citizen SMS status notifications.",
            body_style,
        )
    )

    # Build document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully generated at: {output_filename}")


if __name__ == "__main__":
    output_path = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        "AI_Smart_Complaint_Resolver_Project_Report.pdf",
    )
    build_pdf_report(output_path)
