"""
Generate sample test PDFs for the Multi-Document Research Agent.
Run: python generate_samples.py
Requires: pip install fpdf2
"""

from fpdf import FPDF
import os

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_pdfs")
os.makedirs(SAMPLE_DIR, exist_ok=True)


def create_pdf(filename, title, content_pages):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for page_text in content_pages:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, page_text)

    path = os.path.join(SAMPLE_DIR, filename)
    pdf.output(path)
    print(f"Created: {path}")


# ── Paper 1: AI in Healthcare ──────────────────────────────────────────
create_pdf("ai_healthcare_2024.pdf", "AI in Healthcare: Opportunities and Challenges", [
    """Abstract

Artificial intelligence (AI) is rapidly transforming healthcare delivery. This paper examines 
the current applications of AI in medical diagnosis, drug discovery, and patient care management. 
We find that AI systems can improve diagnostic accuracy by up to 35% compared to traditional methods.

Introduction

The integration of AI into healthcare systems has accelerated significantly in recent years. 
Machine learning algorithms, particularly deep learning models, have demonstrated remarkable 
capabilities in image recognition, natural language processing, and predictive analytics. 
These advancements have opened new possibilities for improving patient outcomes and reducing 
healthcare costs.

Our research indicates that AI adoption in hospitals has increased by 45% between 2020 and 2024, 
with the most significant growth in radiology and pathology departments.""",

    """Results and Analysis

Our comprehensive study across 50 hospitals found the following key results:

1. AI-assisted diagnosis reduced diagnostic errors by 28% in radiology departments.
2. Natural language processing tools improved clinical documentation efficiency by 40%.
3. Predictive models for patient readmission achieved 82% accuracy.
4. Drug interaction detection systems prevented approximately 15,000 adverse events annually.

However, we also identified significant challenges:
- Data privacy concerns remain the primary barrier to AI adoption (cited by 67% of administrators).
- Algorithmic bias was detected in 23% of the AI systems studied.
- The initial implementation cost averages $2.3 million per hospital.

Conclusion

AI has tremendous potential to transform healthcare, but careful attention must be paid to 
ethical considerations, data privacy, and bias mitigation. We recommend a phased approach to 
AI implementation with continuous monitoring and validation."""
])


# ── Paper 2: AI Ethics in Medicine ─────────────────────────────────────
create_pdf("ai_ethics_medicine.pdf", "Ethical Considerations of AI in Medical Practice", [
    """Abstract

This paper critically examines the ethical implications of deploying artificial intelligence 
in medical practice. While AI promises improved efficiency, our analysis reveals significant 
concerns regarding patient autonomy, algorithmic transparency, and equitable access to 
AI-enhanced healthcare.

Introduction

The rapid deployment of AI in healthcare raises fundamental ethical questions. Unlike other 
industries, healthcare AI directly impacts human lives and well-being. Our research surveyed 
200 medical professionals and 500 patients to understand perspectives on AI in medicine.

Key Findings:
- 72% of patients expressed discomfort with AI making autonomous diagnostic decisions.
- Only 34% of AI systems used in hospitals provide explanations for their recommendations.
- Rural and underserved communities have 60% less access to AI-enhanced healthcare services.""",

    """Detailed Analysis

Our study reveals a critical finding that contradicts previous optimistic assessments: 
AI diagnostic systems show a 15% higher error rate when applied to underrepresented 
demographic groups. This challenges the claim that AI universally improves diagnostic accuracy.

Furthermore, the cost-benefit analysis shows that while AI reduces per-diagnosis cost by 
an average of $45, the initial implementation and maintenance costs make AI economically 
unfeasible for hospitals serving fewer than 200 patients daily.

We found that AI adoption has actually decreased by 12% in rural hospitals between 2022 and 
2024, contradicting industry reports of universal growth.

Recommendations

1. Mandatory algorithmic auditing for all medical AI systems
2. Patient consent requirements for AI-assisted diagnosis
3. Government subsidies to ensure equitable access to AI healthcare tools
4. Standardized transparency requirements for AI decision-making processes

Conclusion

The promise of AI in healthcare must be balanced with rigorous ethical oversight. Without 
proper safeguards, AI risks exacerbating existing healthcare inequalities rather than 
resolving them."""
])


# ── Paper 3: Machine Learning for Drug Discovery ──────────────────────
create_pdf("ml_drug_discovery.pdf", "Machine Learning Approaches in Modern Drug Discovery", [
    """Abstract

Machine learning (ML) is revolutionizing the pharmaceutical industry by accelerating drug 
discovery timelines. This paper presents a comprehensive review of ML applications in target 
identification, lead optimization, and clinical trial design. Our meta-analysis of 85 studies 
shows that ML reduces average drug development time by 30-40%.

Introduction

Traditional drug discovery is a lengthy and expensive process, typically requiring 10-15 
years and over $2.6 billion in investment. Machine learning offers the potential to 
significantly reduce both timelines and costs by automating key stages of the discovery pipeline.

Recent advances in deep learning, reinforcement learning, and generative models have enabled 
researchers to predict molecular properties, design novel compounds, and optimize clinical 
trial protocols with unprecedented accuracy.""",

    """Results

Our analysis of ML-driven drug discovery projects reveals several important trends:

1. Generative AI models can propose novel drug candidates 100x faster than traditional screening.
2. ML-based toxicity prediction reduces late-stage drug failures by 25%.
3. AI-optimized clinical trials require 35% fewer participants while maintaining statistical power.
4. The cost of ML-assisted drug development averages $1.8 billion vs $2.6 billion traditionally.

Cross-Domain Observations:
- AI applications in drug discovery share many similarities with AI in diagnostic medicine.
- Both fields benefit from large-scale data availability and transfer learning techniques.
- Privacy and regulatory challenges are common across healthcare AI applications.

The integration of AI across healthcare verticals—from diagnosis to drug development—represents 
a unified trend toward data-driven medicine. However, the pace of adoption varies significantly 
between academic research institutions and commercial pharmaceutical companies.

Conclusion

Machine learning is not merely an incremental improvement but a fundamental paradigm shift 
in drug discovery. Organizations that embrace ML-driven approaches gain a significant 
competitive advantage in bringing therapeutics to market."""
])

print("\nDone! Sample PDFs created in:", SAMPLE_DIR)
