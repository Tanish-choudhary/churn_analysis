# Executive Analytics Capstone Report

**Customer Churn Analysis & Retention Prioritization**

---

## Title Page

**Project:** Executive Analytics Capstone — Customer Churn Analysis & Retention Prioritization
**Prepared by:** Executive Analytics Capstone Internship Team
**Date:** November 2026
**Version:** 1.0
**Classification:** Internal — Business Decision Support

---

## Executive Summary

This capstone project delivers a complete, end-to-end analytics solution for customer churn understanding and retention prioritization. Using a cleaned dataset of **10,000 telecom customers**, we progressed from data quality audit through exploratory analysis, interactive KPI monitoring, customer segmentation, and transparent rule-based risk scoring to produce **actionable, segment-specific retention recommendations**.

**Key Findings:**
- **Overall historical churn rate: 75.06%** — unusually high, requiring urgent attention
- **Four distinct customer segments** identified via K-Means clustering (Churn target excluded)
- **1,833 customers (18.3%) classified as High Risk** using a transparent 0-100 rule-based score
- **$155,849 in monthly recurring revenue** associated with High-Risk customers
- **Illustrative scenario:** A 10% relative churn reduction among High-Risk customers could preserve ~$186K annual revenue

**Recommendation:** Approve a **$750K pilot budget** for 90-day segment-specific retention programs with A/B testing, starting with Senior Vulnerable and Budget-Conscious segments.

**Critical Caveat:** All risk scores are prioritization heuristics, **not predicted probabilities**. Historical patterns do not establish causation. Recommendations require pilot validation before scaling.

---

## Business Problem

### Why Customer Churn Matters
- **Revenue erosion:** Every lost customer represents lost recurring revenue
- **Acquisition cost asymmetry:** New customers cost 5-25x more to acquire than retaining existing ones
- **Competitive risk:** Churned customers often switch to competitors
- **Brand signal:** Sustained high churn indicates systemic unmet needs
- **Planning uncertainty:** Unpredictable revenue undermines financial forecasting

### Business Questions Addressed
1. Which customers are most vulnerable to churn?
2. What characteristics define distinct vulnerable segments?
3. Where should limited retention resources be focused for maximum impact?
4. What specific actions address the root risk factors for each segment?
5. How can we measure the effectiveness of retention interventions?

---

## Data & Analytical Approach

### Dataset
| Metric | Value |
|--------|-------|
| Total Customers | 10,000 |
| Overall Churn Rate | 75.06% |
| Retention Rate | 24.94% |
| Monthly Recurring Revenue | $688,744 |
| Features Available | 17 (demographic, service, financial, behavioral) |

### Data Quality Process
1. **Raw data:** 10,100 records with missing values, dtype issues, duplicates, inconsistent categories
2. **Cleaning:** Median imputation (charges), mode imputation (categorical), deduplication, dtype standardization, outlier flagging (IQR)
3. **Final dataset:** 10,000 clean records, 0 missing values, all columns typed correctly
4. **Reproducibility:** Deterministic pipeline (`scripts/clean_pipeline.py`)

### Analytical Pipeline
| Phase | Method | Key Principle |
|-------|--------|---------------|
| 1. Exploratory Analysis | Descriptive stats, visualizations | Pattern discovery without modeling |
| 2. KPI Dashboard | Streamlit + Plotly | Interactive monitoring & filtering |
| 3. Segmentation | K-Means (K=4) | **Churn target excluded** — no leakage |
| 4. Risk Scoring | Rule-based (7 factors, 0-100) | **Transparent heuristic, not ML** |
| 5. Validation | Historical churn by segment | Retrospective only, not used for creation |

### Features Used for Segmentation (9)
- **Financial:** Tenure, Monthly Charges, Total Charges
- **Service:** Contract Type, Online Security
- **Payment:** Payment Method
- **Demographic:** Senior Citizen, Partner, Dependents

### Features Excluded (Prevent Leakage)
- CustomerID (identifier)
- Churn (target)
- Outlier flags, logical flags (derived columns)

---

## Key Findings

### Exploratory Analysis (Validated Patterns)

| Finding | Evidence |
|---------|----------|
| **Contract type** shows minimal churn differentiation | Month-to-month: 74.65%, One year: 75.07%, Two year: 75.53% |
| **Tenure alone is not protective** | Q1 (0-12 mo): 75.88% churn; Q4 (50+ mo): 76.76% churn |
| **Payment method correlates with risk** | Electronic check users overrepresented in High Risk |
| **Service gaps elevate risk** | No online security → +10 risk points |
| **Senior citizens form a unique risk cluster** | 100% of Senior Vulnerable segment are seniors |

### Customer Segmentation (K=4, Silhouette=0.176)

| Segment | Customers | Share | Avg Tenure | Avg Monthly | Hist. Churn | Avg Risk | % High Risk |
|---------|-----------|-------|------------|-------------|-------------|----------|-------------|
| **Senior Vulnerable** | 1,546 | 15.5% | 34.7 mo | $67.17 | 75.0% | 47.0 | 25.9% |
| **Budget-Conscious** | 3,151 | 31.5% | 28.8 mo | $59.49 | 75.3% | 45.1 | 23.9% |
| **High-Value Long-Term** | 2,343 | 23.4% | 56.2 mo | $91.76 | 76.2% | 41.6 | 13.2% |
| **New Vulnerable** | 2,960 | 29.6% | 28.4 mo | $61.64 | 74.0% | 38.2 | 12.6% |

### Segment Characteristics (Data-Driven)

**1. Senior Vulnerable** (Priority 1)
- 100% senior citizens, month-to-month contracts, electronic check payment, no online security
- Highest % High Risk (25.9%), multiple compounding risk factors

**2. Budget-Conscious** (Priority 2)
- Largest segment (31.5%), lowest monthly charges ($59.49), mailed check payment, have online security
- Risk driven by contract type and payment method

**3. High-Value Long-Term** (Priority 3)
- Highest tenure (56.2 mo), highest charges ($91.76), highest lifetime value ($5,092)
- Despite loyalty indicators, 76.2% historical churn — revenue protection critical

**4. New Vulnerable** (Priority 4)
- Lowest tenure (28.4 mo), auto-pay users, no online security
- Early intervention opportunity before habits solidify

### Risk Prioritization

**Rule-Based Scoring (7 Factors, 0-100):**

| Factor | Max Points | Thresholds |
|--------|------------|------------|
| Tenure | 25 | ≤6 mo: 25, 7-12: 15, 13-24: 10, 25-48: 5, 48+: 0 |
| Monthly Charges | 20 | ≥$90: 20, $70-89: 15, $50-69: 10, $30-49: 5 |
| Contract Type | 25 | Month-to-month: 25, One year: 10, Two year: 0 |
| Payment Method | 10 | Electronic check: 10, Mailed check: 5, Auto: 0 |
| Online Security | 10 | No: 10, No internet: 5, Yes: 0 |
| Senior Citizen | 5 | Yes: 5 |
| No Partner/Dependents | 5 | Both No: 5 |

**Risk Categories:**
- **Low Risk (0-34):** 2,793 customers (27.9%)
- **Medium Risk (35-59):** 5,374 customers (53.7%)
- **High Risk (60-100):** 1,833 customers (18.3%)

**High-Risk Monthly Revenue at Risk: $155,849**

---

## Segment-Wise Risk Breakdown Table

| Segment | Customer Count | Customer Share | Historical Churn Rate | Avg Monthly Charges | Avg Tenure | Avg Risk Score | Recommended Action |
|---------|----------------|----------------|----------------------|---------------------|------------|----------------|---------------------|
| Senior Vulnerable | 1,546 | 15.5% | 75.0% | $67.17 | 34.7 mo | 47.0 | Dedicated senior support, contract upgrade incentive, auto-pay migration, security bundle |
| Budget-Conscious | 3,151 | 31.5% | 75.3% | $59.49 | 28.8 mo | 45.1 | Value tier launch, annual discount, auto-pay nudge, usage alerts |
| High-Value Long-Term | 2,343 | 23.4% | 76.2% | $91.76 | 56.2 mo | 41.6 | Loyalty program, price protection, dedicated account manager, premium perks |
| New Vulnerable | 2,960 | 29.6% | 74.0% | $61.64 | 28.4 mo | 38.2 | Structured onboarding, default-on security, first-year contract incentive, early warning |

---

## Prioritized Recommendations

### Priority 1: Senior Vulnerable (1,546 customers)
| Aspect | Detail |
|--------|--------|
| **Characteristics** | 100% seniors, month-to-month, electronic check, no security, 34.7 mo tenure |
| **Business Concern** | Multiple compounding risk factors; highest % High Risk (25.9%) |
| **Retention Action** | Dedicated senior support line; 20% contract upgrade discount; guided auto-pay migration; free security bundle; quarterly proactive calls |
| **Communication Strategy** | Phone-first, high-touch, empathetic; avoid digital-only channels |
| **KPI** | High-Risk % reduction; contract upgrade rate; support satisfaction |
| **Pilot Duration** | 90 days |

### Priority 2: Budget-Conscious (3,151 customers)
| Aspect | Detail |
|--------|--------|
| **Characteristics** | Largest segment, lowest charges ($59.49), mailed check, has security, 28.8 mo tenure |
| **Business Concern** | Price sensitivity + manual payment = volatility risk |
| **Retention Action** | "Essentials" tier at ~$45/mo; 15% annual discount ($50.60 effective); auto-pay credit ($5/mo × 3 mo); usage alerts |
| **Communication Strategy** | Value-focused, digital-first (email/SMS/app), self-service options |
| **KPI** | Plan migration rate; auto-pay adoption; churn rate vs control |
| **Pilot Duration** | 90 days |

### Priority 3: High-Value Long-Term (2,343 customers)
| Aspect | Detail |
|--------|--------|
| **Characteristics** | Highest value ($91.76/mo, $5,092 lifetime), 56.2 mo tenure, has security, 76.2% churn |
| **Business Concern** | Revenue concentration risk; losing these is disproportionately costly |
| **Retention Action** | Tiered loyalty program; 24-month price lock; dedicated account managers (top 20%); premium security + device upgrades; win-back protocol |
| **Communication Strategy** | Relationship-based, proactive recognition, exclusive channels |
| **KPI** | Revenue retention rate; NPS; upgrade/cross-sell uptake |
| **Pilot Duration** | 90 days |

### Priority 4: New Vulnerable (2,960 customers)
| Aspect | Detail |
|--------|--------|
| **Characteristics** | Lowest tenure (28.4 mo), auto-pay, no security, 28.4 mo tenure, 74.0% churn |
| **Business Concern** | Early churn cascade; onboarding gaps compound over lifetime |
| **Retention Action** | 30/60/90 day onboarding; default-on security (opt-out); first-year contract auto-convert at month 4; early warning (>2 tickets = outreach) |
| **Communication Strategy** | Digital-native, app/in-app messaging, automated but personalized |
| **KPI** | 90-day retention; security adoption; support ticket volume; contract conversion |
| **Pilot Duration** | 90 days |

### Cross-Segment Quick Wins (Immediate)
| Action | Effort | Impact | Timeline |
|--------|--------|--------|----------|
| Migrate electronic check → auto-pay | Low | High | 30 days |
| Enable online security by default | Low | Medium | 14 days |
| Add risk score to CRM for agents | Medium | High | 60 days |
| Monthly segment churn dashboard | Low | Medium | 30 days |

---

## Expected Business Impact

### Illustrative Scenario: 10% Relative Churn Reduction Among High-Risk Customers

| Metric | Value | Basis |
|--------|-------|-------|
| High-Risk Customers | 1,833 | Actual count (Risk_Category = High Risk) |
| Assumed Relative Churn Reduction | 10% | Illustrative assumption for scenario planning |
| Estimated Customers Retained | 183 | 1,833 × 10% |
| Avg Monthly Charges (High Risk) | ~$85 | Weighted average from segment data |
| **Monthly Revenue Preserved** | **~$15,500** | 183 × $85 |
| **Annual Revenue Preserved** | **~$186,000** | Monthly × 12 |

### Investment vs. Return (Illustrative)

| Initiative | Est. Cost | High-Risk Customers | Est. Retained (10%) | Annual Revenue Saved |
|------------|-----------|---------------------|---------------------|---------------------|
| Senior program | $150K | 400 | 40 | ~$350K |
| Budget value plan | $200K | 750 | 75 | ~$540K |
| Loyalty program | $300K | 310 | 31 | ~$850K |
| Onboarding overhaul | $100K | 370 | 37 | ~$270K |
| **Total** | **$750K** | **1,830** | **183** | **~$2.0M** |

### Assumptions & Caveats
- ⚠ **Illustrative only** — not a forecast or guarantee
- Assumes 10% relative uplift on High-Risk churn only (conservative)
- Average annual revenue per customer estimated from monthly charges ($700-$1,100 range)
- Does not account for implementation costs beyond pilot budget
- Requires A/B test validation before any investment decision
- External factors (competitors, economy) not modeled

---

## Limitations & Responsible Interpretation

| Limitation | Implication |
|------------|-------------|
| **Historical data ≠ future behavior** | Patterns may shift; quarterly refresh essential |
| **K-Means encoding sensitivity** | Label Encoding used; One-Hot tested separately; results may differ |
| **Risk score is heuristic** | Not a predicted probability; no calibration to actual churn likelihood |
| **Segments are descriptive** | Cluster assignments don't predict future segment membership |
| **No causal evidence** | Changing a risk factor (e.g., adding security) may not reduce churn |
| **75% overall churn unusually high** | Validate against current production data before acting |
| **Static snapshot** | Single point-in-time; customer behavior evolves |
| **External factors omitted** | Competitor actions, economic conditions, life events not captured |
| **Illustrative impact scenarios** | Not guaranteed results; require pilot validation |

### Responsible Use Guidelines
1. **Never present risk scores as churn probabilities**
2. **Always pair recommendations with pilot validation plans**
3. **Segment names are analytical constructs** — avoid using them in customer-facing communications
4. **Senior citizen status used analytically** — ensure compliance with age discrimination regulations in any outreach
5. **Monitor for unintended consequences** — e.g., auto-pay pressure on vulnerable customers

---

## Implementation Roadmap

| Phase | Timeline | Actions | Owner |
|-------|----------|---------|-------|
| **Immediate** | Week 1-2 | CRM integration of Risk_Score/Risk_Category; support team training | IT / Analytics |
| **Short-term** | Month 1 | Automated daily risk scoring; segment-level dashboards; quick wins launch | Analytics / Ops |
| **Pilot** | Quarter 1 | A/B test retention offers by segment; validate risk score vs 90-day outcomes; calibrate thresholds | Analytics / Marketing |
| **Scale** | Ongoing | Quarterly segment refresh; expand winning pilots; sunset losers | All |

### Decisions Required
| Decision | Owner | Deadline |
|----------|-------|----------|
| Approve pilot budget ($750K) | VP Retention | Dec 1 |
| Assign segment ownership | Dir. Customer Success | Dec 1 |
| Integrate risk scores into CRM | IT / Analytics | Jan 15 |
| Design A/B test framework | Analytics | Jan 15 |
| Quarterly refresh schedule | Analytics | Ongoing |

---

## Appendix: References

### Project Assets
- **Interactive Dashboard:** `app.py` — Run with `streamlit run app.py`
- **Segmentation Notebook:** `notebooks/segmentation_and_risk_model_executed.ipynb`
- **EDA Notebook:** `notebooks/analysis.ipynb`
- **Customer-Level Data:** `data/customer_segmented.csv`
- **Segment Summary:** `reports/segment_summary.csv`
- **Detailed Analysis:** `reports/segment_analysis.md`
- **Recommendation Memo:** `reports/recommendation_memo.md`
- **Data Quality Summary:** `reports/data_quality_summary.md`
- **Executive Visualizations:** `reports/executive_visualizations/`
- **Presentation:** `reports/executive_capstone_presentation.pptx`
- **Presentation Script:** `reports/executive_presentation_script.md`
- **Metrics Summary:** `reports/executive_metrics_summary.csv`

### GitHub Repository
[Link to repository — add when available]

---

*End of Report*