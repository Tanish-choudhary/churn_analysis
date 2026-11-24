# Business KPI Dashboard & Customer Segmentation Analysis & Executive Capstone

This project provides a comprehensive customer churn analysis platform with:
- **Step 1-3:** Business KPI Dashboard (Streamlit)
- **Step 4:** Customer Segmentation and Explainable Churn-Risk Prioritization Model
- **Step 5:** Executive Analytics Capstone — Presentation, Report & Business Impact Analysis

---

## Step 1-3: Business KPI Dashboard

Interactive Streamlit dashboard for real-time churn metrics.

### Features
- **KPI Metrics**: Overall Churn Rate, Retention Rate, Revenue at Risk (Monthly), Average Historical Customer Charges
- **Interactive Filtering**: Filter by Contract Type, Tenure range, Monthly Charges
- **Visualizations**: 
  - Churn Rate by Contract Type
  - Churn Distribution by Tenure
  - Revenue at Risk per Contract
  - Customer Segmentation Analysis (Spending vs Tenure)
- **Automatic Insights**: Business insights based on filtered data

### How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Step 4: Customer Segmentation & Explainable Risk Scoring

Advanced analytics moving from descriptive to actionable customer segmentation and churn-risk prioritization.

### Deliverables

| File | Description |
|------|-------------|
| `notebooks/segmentation_and_risk_model.ipynb` | Complete executable notebook with all analysis |
| `data/customer_segmented.csv` | Original data + Cluster ID, Segment Name, Risk Score, Risk Category |
| `reports/segment_summary.csv` | Segment-level summary statistics |
| `reports/segment_analysis.md` | Detailed methodology, segment definitions, limitations |
| `reports/recommendation_memo.md` | Executive recommendation memo with prioritized actions |
| `reports/segmentation_visualizations/` | All generated charts (PNG) |

### Segmentation Approach

**Method:** K-Means clustering (K=4) on 9 features:
- **Financial:** Tenure, Monthly Charges, Total Charges
- **Service:** Contract Type, Online Security
- **Payment:** Payment Method
- **Demographic:** Senior Citizen, Partner, Dependents

**Preprocessing:**
- Numerical features: StandardScaler (zero mean, unit variance)
- Categorical features: Label Encoding
- **Churn target EXCLUDED** — prevents data leakage

**Cluster Selection:** Elbow Method + Silhouette Score (K=4 selected)

### Segment Definitions

| Cluster | Segment Name | Customers | Key Characteristics |
|---------|-------------|-----------|---------------------|
| 0 | Senior Vulnerable | 1,546 (15.5%) | 100% seniors, month-to-month, electronic check, no security |
| 1 | Budget-Conscious | 3,151 (31.5%) | Lowest charges, mailed check, has security |
| 2 | High-Value Long-Term | 2,343 (23.4%) | Highest tenure/charges, has security |
| 3 | New Vulnerable | 2,960 (29.6%) | Lowest tenure, auto-pay, no security |

### Risk Scoring Logic

**Transparent rule-based score (0-100)** — No Churn column used.

| Risk Factor | Conditions | Max Points |
|-------------|------------|------------|
| Tenure | ≤6 mo: 25, 7-12: 15, 13-24: 10, 25-48: 5, 48+: 0 | 25 |
| Monthly Charges | ≥$90: 20, $70-89: 15, $50-69: 10, $30-49: 5, <$30: 0 | 20 |
| Contract | Month-to-month: 25, One year: 10, Two year: 0 | 25 |
| Payment Method | Electronic check: 10, Mailed check: 5, Auto: 0 | 10 |
| Online Security | No: 10, No internet: 5, Yes: 0 | 10 |
| Senior Citizen | Yes: 5 | 5 |
| No Partner/Dependents | Both No: 5 | 5 |
| **TOTAL** | | **100** |

**Risk Categories:**
- **Low Risk:** 0-34 (27.9% of customers)
- **Medium Risk:** 35-59 (53.7%)
- **High Risk:** 60-100 (18.3%)

### How to Run the Notebook

```bash
# Install additional dependencies
pip install matplotlib seaborn scikit-learn

# Run notebook
jupyter notebook notebooks/segmentation_and_risk_model.ipynb
```

Or execute the analysis script:
```bash
python scripts/generate_visualizations.py
```

### Generated Visualizations

All saved to `reports/segmentation_visualizations/`:
1. `segment_distribution.png` — Customer count per segment
2. `avg_risk_by_segment.png` — Average risk score by segment
3. `segmentation_pca.png` — PCA projection of clusters
4. `risk_category_distribution.png` — Overall and by-segment risk distribution
5. `characteristics_comparison.png` — Box plots of tenure, charges, risk by segment
6. `churn_by_segment.png` — Historical churn rate by segment
7. `risk_score_churn_distribution.png` — Risk score distribution for churned vs retained
8. `cluster_selection.png` — Elbow and silhouette analysis

### Business Recommendations Summary

**Priority 1 — Senior Vulnerable:** Dedicated support line, contract upgrade incentives, auto-pay migration, free security bundle

**Priority 2 — Budget-Conscious:** Value tier plan, annual commitment discount, auto-pay nudges, usage alerts

**Priority 3 — High-Value Long-Term:** Loyalty program, price protection, dedicated account managers, premium perks

**Priority 4 — New Vulnerable:** Structured 30/60/90 onboarding, default-on security, first-year contract incentive, early warning system

### Model Limitations

1. **Not a predictive model** — Risk score is heuristic, not a probability
2. **No causal claims** — Correlations only; interventions should be tested
3. **Descriptive clustering** — Segments don't predict future behavior
4. **Static snapshot** — Refresh quarterly with new data
5. **No external validation** — Test on holdout/out-of-time data before production use
6. **Threshold sensitivity** — Business context should guide final thresholds

---

## Step 5: Executive Analytics Capstone

Professional executive presentation package for business decision-makers.

### Deliverables

| File | Description |
|------|-------------|
| `reports/executive_capstone_presentation.pptx` | 11-slide PowerPoint presentation (~10 min) |
| `reports/executive_capstone_report.pdf` | 13-page professional PDF report |
| `reports/executive_capstone_report.md` | Source Markdown for the report |
| `reports/executive_presentation_script.md` | Speaker notes with timing (~10 min) |
| `reports/executive_metrics_summary.csv` | All verified metrics with sources |
| `reports/executive_visualizations/` | 12 presentation-ready charts (PNG) |

### Presentation Structure (11 Slides, ~10 Minutes)

| Slide | Title | Key Content |
|-------|-------|-------------|
| 1 | Title & Business Objective | Project name, objective, team, date |
| 2 | The Business Problem | Why churn matters, acquisition cost asymmetry, key questions |
| 3 | Data Quality & Analytical Foundation | 10K customers, 75.06% churn, pipeline, no-leakage principle |
| 4 | Key Findings from EDA | Contract, tenure, payment, security, senior patterns |
| 5 | Business KPI Dashboard | Interactive Streamlit, KPIs, filters, monitoring |
| 6 | Customer Segmentation | 4 segments, counts, radar chart, profile table |
| 7 | Risk Prioritization | 0-100 rule-based score, 7 factors, 3 categories, $155K at risk |
| 8 | Segment-Specific Recommendations | 4 priority segments, actions, KPIs, quick wins |
| 9 | Expected Business Impact | Illustrative 10% High-Risk reduction = ~$186K/yr |
| 10 | Implementation Roadmap & Limitations | 30/60/90 day plan, 9 limitations, decisions needed |
| 11 | Conclusion | 3 takeaways, $750K pilot decision request |

### Report Contents

1. **Executive Summary** — Key findings, recommendation, caveat
2. **Business Problem** — Why churn matters, key questions
3. **Data & Analytical Approach** — Dataset, quality, pipeline, features
4. **Key Findings** — EDA patterns, segment table, risk scoring logic
5. **Segment-Wise Risk Breakdown** — Verified metrics table
6. **Prioritized Recommendations** — 4 segments, actions, KPIs, pilot duration
7. **Expected Business Impact** — Illustrative scenario with assumptions
8. **Limitations & Responsible Interpretation** — 9 limitations, guidelines
9. **Implementation Roadmap** — Phases, decisions, owners
10. **Appendix** — All project assets with paths

### Verified Metrics Summary

| Metric | Value | Source |
|--------|-------|--------|
| Total Customers | 10,000 | `data/churn_clean.csv` |
| Overall Churn Rate | 75.06% | `data/churn_clean.csv` |
| Retention Rate | 24.94% | `data/churn_clean.csv` |
| Monthly Revenue | $688,744 | `data/customer_segmented.csv` |
| High Risk Customers | 1,833 (18.3%) | `data/customer_segmented.csv` |
| Monthly Rev at Risk (High) | $155,849 | `data/customer_segmented.csv` |
| K-Means Clusters | 4 (Silhouette=0.176) | Notebook |
| Illustrative 10% Reduction | 183 retained, ~$186K/yr | Calculated (ILLUSTRATIVE) |

### Executive Visualizations (12 charts)

All saved to `reports/executive_visualizations/`:
1. `kpi_churn_retention.png` — Overall churn vs retention pie
2. `revenue_by_risk.png` — Monthly revenue by risk category (horizontal bar)
3. `segment_distribution.png` — Customer count by segment
4. `churn_by_segment.png` — Historical churn rate by segment
5. `risk_score_by_segment.png` — Average risk score by segment with thresholds
6. `risk_category_distribution.png` — Risk category pie with legend
7. `churn_by_contract.png` — Churn rate by contract type
8. `churn_by_tenure.png` — Churn rate by tenure quartile
9. `segment_radar.png` — Normalized segment profile comparison
10. `impact_scenario.png` — Illustrative 10% High-Risk reduction
11. `revenue_by_segment.png` — Monthly revenue contribution by segment
12. `roadmap.png` — Implementation timeline

---

## Project Structure

```
churn_analysis/
├── app.py                                      # Streamlit KPI Dashboard
├── requirements.txt                            # Python dependencies
├── README.md                                   # This file
├── data/
│   ├── churn_clean.csv                        # Original cleaned dataset (10,000 rows)
│   └── customer_segmented.csv                 # + Cluster_ID, Segment, Risk_Score, Risk_Category
├── notebooks/
│   ├── analysis.ipynb                         # Original EDA notebook
│   ├── segmentation_and_risk_model.ipynb      # Step 4 complete notebook
│   └── segmentation_and_risk_model_executed.ipynb  # Executed notebook with outputs
├── reports/
│   ├── data_quality_summary.md
│   ├── quality_decision_log.json
│   ├── segment_summary.csv                    # Segment-level statistics
│   ├── segment_analysis.md                    # Detailed methodology
│   ├── recommendation_memo.md                 # Executive memo
│   ├── segmentation_visualizations/           # Step 4 charts (8 PNG)
│   ├── executive_capstone_presentation.pptx   # Step 5 presentation
│   ├── executive_capstone_report.pdf          # Step 5 PDF report
│   ├── executive_capstone_report.md           # Step 5 report source
│   ├── executive_presentation_script.md       # Step 5 speaker notes
│   ├── executive_metrics_summary.csv          # Step 5 verified metrics
│   └── executive_visualizations/              # Step 5 charts (12 PNG)
└── scripts/
    ├── generate_visualizations.py
    ├── create_executive_visualizations.py
    ├── create_presentation.py
    └── create_pdf_report.py
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install matplotlib seaborn scikit-learn python-pptx fpdf2

# 2. Run KPI Dashboard (Steps 1-3)
streamlit run app.py

# 3. Run Segmentation Analysis (Step 4)
jupyter notebook notebooks/segmentation_and_risk_model.ipynb
# OR
python scripts/generate_visualizations.py

# 4. Generate Step 5 Executive Deliverables
python scripts/create_executive_visualizations.py
python scripts/create_presentation.py
python scripts/create_pdf_report.py
```

---

## Requirements

- Python 3.8+
- pandas, numpy
- streamlit, plotly (dashboard)
- matplotlib, seaborn (visualizations)
- scikit-learn (clustering, preprocessing)
- python-pptx (presentation generation)
- fpdf2 (PDF report generation)

Install all:
```bash
pip install pandas numpy streamlit plotly matplotlib seaborn scikit-learn python-pptx fpdf2
```