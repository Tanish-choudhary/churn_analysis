from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 5, 'Executive Analytics Capstone - Customer Churn Analysis', 0, 0, 'L')
            self.cell(0, 5, f'Page {self.page_no()}', 0, 1, 'R')
            self.line(10, 12, 200, 12)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'CONFIDENTIAL - Internal Use Only', 0, 0, 'C')

    def section_title(self, title, level=1):
        if level == 1:
            self.set_font('Helvetica', 'B', 16)
            self.set_text_color(44, 62, 80)
            self.ln(4)
            self.cell(0, 10, title, 0, 1)
            self.set_draw_color(44, 62, 80)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)
        elif level == 2:
            self.set_font('Helvetica', 'B', 13)
            self.set_text_color(52, 73, 94)
            self.ln(3)
            self.cell(0, 8, title, 0, 1)
            self.ln(2)
        elif level == 3:
            self.set_font('Helvetica', 'BI', 11)
            self.set_text_color(44, 62, 80)
            self.ln(2)
            self.cell(0, 7, title, 0, 1)
            self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(44, 62, 80)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text, indent=15):
        x = self.get_x()
        self.set_font('Helvetica', '', 10)
        self.set_text_color(44, 62, 80)
        self.cell(indent, 5, '')
        self.cell(5, 5, '-')
        self.multi_cell(0, 5, text)
        self.ln(1)

    def bold_bullet(self, bold_part, normal_part, indent=15):
        self.cell(indent, 5, '')
        self.set_font('Helvetica', '', 10)
        self.set_text_color(44, 62, 80)
        self.cell(5, 5, '-')
        self.set_font('Helvetica', 'B', 10)
        self.write(5, bold_part)
        self.set_font('Helvetica', '', 10)
        self.write(5, normal_part)
        self.ln(6)

    def kpi_row(self, labels, values, colors=None):
        w = (190 - 20) / len(labels)
        self.ln(2)
        for i, (label, value) in enumerate(zip(labels, values)):
            self.set_font('Helvetica', 'B', 11)
            self.set_text_color(100, 100, 100)
            self.cell(w, 6, label, 0, 0, 'C')
            self.ln(6)
            self.set_font('Helvetica', 'B', 18)
            if colors:
                self.set_text_color(*colors[i])
            else:
                self.set_text_color(44, 62, 80)
            self.cell(w, 10, value, 0, 0, 'C')
            self.ln(10)
        self.ln(5)
        self.set_x(10)

    def add_table(self, headers, data, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)

        # Header
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(44, 62, 80)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, 1, 0, 'C', True)
        self.ln()

        # Data
        self.set_font('Helvetica', '', 8)
        self.set_text_color(44, 62, 80)
        fill = False
        for row in data:
            if fill:
                self.set_fill_color(236, 240, 241)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6, str(cell), 1, 0, 'C', True)
            self.ln()
            fill = not fill
        self.ln(4)

pdf = PDF()
pdf.set_title('Executive Analytics Capstone - Customer Churn Analysis')
pdf.set_author('Executive Analytics Capstone Internship Team')

# ============================================================
# TITLE PAGE
# ============================================================
pdf.add_page()
pdf.ln(30)
pdf.set_font('Helvetica', 'B', 28)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 15, 'Executive Analytics Capstone', 0, 1, 'C')
pdf.set_font('Helvetica', 'B', 22)
pdf.cell(0, 12, 'Customer Churn Analysis &', 0, 1, 'C')
pdf.cell(0, 12, 'Retention Prioritization', 0, 1, 'C')
pdf.ln(10)
pdf.set_draw_color(44, 62, 80)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(10)
pdf.set_font('Helvetica', '', 14)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, 'Prepared by: Executive Analytics Capstone Internship Team', 0, 1, 'C')
pdf.cell(0, 8, 'Date: November 2026', 0, 1, 'C')
pdf.cell(0, 8, 'Version: 1.0', 0, 1, 'C')
pdf.cell(0, 8, 'Classification: Internal - Business Decision Support', 0, 1, 'C')
pdf.ln(20)
pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(128, 128, 128)
pdf.cell(0, 6, 'CONFIDENTIAL - Internal Use Only', 0, 1, 'C')

# ============================================================
# EXECUTIVE SUMMARY
# ============================================================
pdf.add_page()
pdf.section_title('Executive Summary')

pdf.body_text(
    'This capstone project delivers a complete, end-to-end analytics solution for customer churn '
    'understanding and retention prioritization. Using a cleaned dataset of 10,000 telecom customers, '
    'we progressed from data quality audit through exploratory analysis, interactive KPI monitoring, '
    'customer segmentation, and transparent rule-based risk scoring to produce actionable, '
    'segment-specific retention recommendations.'
)

pdf.section_title('Key Findings', level=2)
pdf.bullet('Overall historical churn rate: 75.06% - unusually high, requiring urgent attention')
pdf.bullet('Four distinct customer segments identified via K-Means clustering (Churn target excluded)')
pdf.bullet('1,833 customers (18.3%) classified as High Risk using a transparent 0-100 rule-based score')
pdf.bullet('$155,849 in monthly recurring revenue associated with High-Risk customers')
pdf.bullet('Illustrative scenario: A 10% relative churn reduction among High-Risk customers could preserve ~$186K annual revenue')

pdf.section_title('Recommendation', level=2)
pdf.body_text(
    'Approve a $750K pilot budget for 90-day segment-specific retention programs with A/B testing, '
    'starting with Senior Vulnerable and Budget-Conscious segments.'
)

pdf.section_title('Critical Caveat', level=2)
pdf.body_text(
    'All risk scores are prioritization heuristics, NOT predicted probabilities. Historical patterns '
    'do not establish causation. Recommendations require pilot validation before scaling.'
)

# ============================================================
# BUSINESS PROBLEM
# ============================================================
pdf.add_page()
pdf.section_title('Business Problem')

pdf.section_title('Why Customer Churn Matters', level=2)
pdf.bullet('Revenue erosion: Every lost customer = lost recurring revenue')
pdf.bullet('Acquisition cost: New customers cost 5-25x more to acquire than retaining existing ones')
pdf.bullet('Competitive risk: Churned customers often switch to competitors')
pdf.bullet('Brand signal: High churn indicates unmet needs or poor experience')
pdf.bullet('Operational impact: Unpredictable revenue makes planning difficult')

pdf.section_title('Key Business Questions', level=2)
pdf.bullet('Which customers are most likely to leave?')
pdf.bullet('What characteristics define vulnerable customer groups?')
pdf.bullet('Where should we focus limited retention resources?')
pdf.bullet('What actions address the root risk factors?')
pdf.bullet('How do we measure the impact of interventions?')

# ============================================================
# DATA & ANALYTICAL APPROACH
# ============================================================
pdf.add_page()
pdf.section_title('Data & Analytical Approach')

pdf.section_title('Dataset Overview', level=2)
pdf.kpi_row(
    ['Total Customers', 'Overall Churn Rate', 'Retention Rate', 'Monthly Revenue'],
    ['10,000', '75.06%', '24.94%', '$688,744']
)

pdf.section_title('Data Quality Process', level=2)
pdf.bullet('Raw dataset: 10,100 records -> 10,000 clean records after deduplication')
pdf.bullet('Missing values: Imputed using median (charges) and mode (categorical)')
pdf.bullet('Data types: Standardized - numeric charges, categorical labels cleaned')
pdf.bullet('Outliers: Flagged via IQR method, preserved for transparency')
pdf.bullet('Logical consistency: TotalCharges validated against tenure x monthly charges')

pdf.section_title('Analytical Pipeline', level=2)
pdf.add_table(
    ['Phase', 'Method', 'Key Principle'],
    [
        ['1. Exploratory Analysis', 'Descriptive stats, visualizations', 'Pattern discovery without modeling'],
        ['2. KPI Dashboard', 'Streamlit + Plotly', 'Interactive monitoring & filtering'],
        ['3. Segmentation', 'K-Means (K=4)', 'Churn target excluded - no leakage'],
        ['4. Risk Scoring', 'Rule-based (7 factors, 0-100)', 'Transparent heuristic, not ML'],
        ['5. Validation', 'Historical churn by segment', 'Retrospective only, not used for creation']
    ],
    col_widths=[30, 60, 100]
)

pdf.section_title('Features Used for Segmentation (9)', level=2)
pdf.bullet('Financial: Tenure, Monthly Charges, Total Charges')
pdf.bullet('Service: Contract Type, Online Security')
pdf.bullet('Payment: Payment Method')
pdf.bullet('Demographic: Senior Citizen, Partner, Dependents')

pdf.section_title('Features Excluded (Prevent Leakage)', level=2)
pdf.bullet('CustomerID (identifier), Churn (target), Outlier flags, Logical flags (derived columns)')

# ============================================================
# KEY FINDINGS
# ============================================================
pdf.add_page()
pdf.section_title('Key Findings')

pdf.section_title('Exploratory Analysis - Validated Patterns', level=2)
pdf.add_table(
    ['Finding', 'Evidence'],
    [
        ['Contract type shows minimal churn differentiation', 'Month-to-month: 74.65%, One year: 75.07%, Two year: 75.53%'],
        ['Tenure alone is not protective', 'Q1 (0-12 mo): 75.88% churn; Q4 (50+ mo): 76.76% churn'],
        ['Payment method correlates with risk', 'Electronic check users overrepresented in High Risk'],
        ['Service gaps elevate risk', 'No online security -> +10 risk points'],
        ['Senior citizens form unique risk cluster', '100% of Senior Vulnerable segment are seniors']
    ],
    col_widths=[70, 120]
)

pdf.section_title('Customer Segmentation (K=4, Silhouette=0.176)', level=2)
pdf.add_table(
    ['Segment', 'Customers', 'Share', 'Avg Tenure', 'Avg Monthly', 'Hist. Churn', 'Avg Risk', '% High Risk'],
    [
        ['Senior Vulnerable', '1,546', '15.5%', '34.7 mo', '$67.17', '75.0%', '47.0', '25.9%'],
        ['Budget-Conscious', '3,151', '31.5%', '28.8 mo', '$59.49', '75.3%', '45.1', '23.9%'],
        ['High-Value Long-Term', '2,343', '23.4%', '56.2 mo', '$91.76', '76.2%', '41.6', '13.2%'],
        ['New Vulnerable', '2,960', '29.6%', '28.4 mo', '$61.64', '74.0%', '38.2', '12.6%']
    ],
    col_widths=[32, 18, 15, 22, 25, 22, 20, 22]
)

pdf.section_title('Segment Characteristics (Data-Driven)', level=2)

pdf.section_title('1. Senior Vulnerable (Priority 1)', level=3)
pdf.bullet('100% senior citizens, month-to-month contracts, electronic check payment, no online security')
pdf.bullet('Highest % High Risk (25.9%), multiple compounding risk factors')
pdf.bullet('34.7 mo avg tenure, $67.17 avg monthly charges')

pdf.section_title('2. Budget-Conscious (Priority 2)', level=3)
pdf.bullet('Largest segment (31.5%), lowest monthly charges ($59.49), mailed check payment, have online security')
pdf.bullet('Risk driven by contract type and payment method')
pdf.bullet('28.8 mo avg tenure, $59.49 avg monthly charges')

pdf.section_title('3. High-Value Long-Term (Priority 3)', level=3)
pdf.bullet('Highest tenure (56.2 mo), highest charges ($91.76), highest lifetime value ($5,092)')
pdf.bullet('Despite loyalty indicators, 76.2% historical churn - revenue protection critical')
pdf.bullet('56.2 mo avg tenure, $91.76 avg monthly charges')

pdf.section_title('4. New Vulnerable (Priority 4)', level=3)
pdf.bullet('Lowest tenure (28.4 mo), auto-pay users, no online security')
pdf.bullet('Early intervention opportunity before habits solidify')
pdf.bullet('28.4 mo avg tenure, $61.64 avg monthly charges')

pdf.section_title('Risk Prioritization', level=2)

pdf.section_title('Rule-Based Scoring (7 Factors, 0-100)', level=3)
pdf.add_table(
    ['Factor', 'Max Points', 'Thresholds'],
    [
        ['Tenure', '25', '<=6 mo: 25, 7-12: 15, 13-24: 10, 25-48: 5, 48+: 0'],
        ['Monthly Charges', '20', '>=$90: 20, $70-89: 15, $50-69: 10, $30-49: 5'],
        ['Contract Type', '25', 'Month-to-month: 25, One year: 10, Two year: 0'],
        ['Payment Method', '10', 'Electronic check: 10, Mailed check: 5, Auto: 0'],
        ['Online Security', '10', 'No: 10, No internet: 5, Yes: 0'],
        ['Senior Citizen', '5', 'Yes: 5'],
        ['No Partner/Dependents', '5', 'Both No: 5']
    ],
    col_widths=[35, 20, 135]
)

pdf.section_title('Risk Categories', level=3)
pdf.bullet('Low Risk (0-34): 2,793 customers (27.9%)')
pdf.bullet('Medium Risk (35-59): 5,374 customers (53.7%)')
pdf.bullet('High Risk (60-100): 1,833 customers (18.3%)')
pdf.bullet('High-Risk Monthly Revenue at Risk: $155,849')

pdf.body_text('IMPORTANT: This is a prioritization heuristic, NOT a predicted probability of churn.')

# ============================================================
# SEGMENT-WISE RISK BREAKDOWN
# ============================================================
pdf.add_page()
pdf.section_title('Segment-Wise Risk Breakdown Table')

pdf.add_table(
    ['Segment', 'Count', 'Share', 'Hist. Churn', 'Avg Monthly', 'Avg Tenure', 'Avg Risk', 'Recommended Action'],
    [
        ['Senior Vulnerable', '1,546', '15.5%', '75.0%', '$67.17', '34.7 mo', '47.0', 'Dedicated support, contract upgrade, auto-pay migration, security bundle'],
        ['Budget-Conscious', '3,151', '31.5%', '75.3%', '$59.49', '28.8 mo', '45.1', 'Value tier, annual discount, auto-pay nudge, usage alerts'],
        ['High-Value Long-Term', '2,343', '23.4%', '76.2%', '$91.76', '56.2 mo', '41.6', 'Loyalty program, price protection, account manager, premium perks'],
        ['New Vulnerable', '2,960', '29.6%', '74.0%', '$61.64', '28.4 mo', '38.2', 'Structured onboarding, default-on security, first-year incentive, early warning']
    ],
    col_widths=[30, 18, 15, 22, 22, 22, 18, 43]
)

# ============================================================
# PRIORITIZED RECOMMENDATIONS
# ============================================================
pdf.add_page()
pdf.section_title('Prioritized Recommendations')

segments = [
    ('Priority 1: Senior Vulnerable (1,546 customers)', [
        ('Characteristics', '100% seniors, month-to-month, electronic check, no security, 34.7 mo tenure'),
        ('Business Concern', 'Multiple compounding risk factors; highest % High Risk (25.9%)'),
        ('Retention Action', 'Dedicated senior support line; 20% contract upgrade discount; guided auto-pay migration; free security bundle; quarterly proactive calls'),
        ('Communication Strategy', 'Phone-first, high-touch, empathetic; avoid digital-only channels'),
        ('KPI', 'High-Risk % reduction; contract upgrade rate; support satisfaction'),
        ('Pilot Duration', '90 days')
    ]),
    ('Priority 2: Budget-Conscious (3,151 customers)', [
        ('Characteristics', 'Largest segment, lowest charges ($59.49), mailed check, has security, 28.8 mo tenure'),
        ('Business Concern', 'Price sensitivity + manual payment = volatility risk'),
        ('Retention Action', '"Essentials" tier at ~$45/mo; 15% annual discount ($50.60 effective); auto-pay credit ($5/mo x 3 mo); usage alerts'),
        ('Communication Strategy', 'Value-focused, digital-first (email/SMS/app), self-service options'),
        ('KPI', 'Plan migration rate; auto-pay adoption; churn rate vs control'),
        ('Pilot Duration', '90 days')
    ]),
    ('Priority 3: High-Value Long-Term (2,343 customers)', [
        ('Characteristics', 'Highest value ($91.76/mo, $5,092 lifetime), 56.2 mo tenure, has security, 76.2% churn'),
        ('Business Concern', 'Revenue concentration risk; losing these is disproportionately costly'),
        ('Retention Action', 'Tiered loyalty program; 24-month price lock; dedicated account managers (top 20%); premium security + device upgrades; win-back protocol'),
        ('Communication Strategy', 'Relationship-based, proactive recognition, exclusive channels'),
        ('KPI', 'Revenue retention rate; NPS; upgrade/cross-sell uptake'),
        ('Pilot Duration', '90 days')
    ]),
    ('Priority 4: New Vulnerable (2,960 customers)', [
        ('Characteristics', 'Lowest tenure (28.4 mo), auto-pay, no security, 74.0% churn'),
        ('Business Concern', 'Early churn cascade; onboarding gaps compound over lifetime'),
        ('Retention Action', '30/60/90 day onboarding; default-on security (opt-out); first-year contract auto-convert at month 4; early warning (>2 tickets = outreach)'),
        ('Communication Strategy', 'Digital-native, app/in-app messaging, automated but personalized'),
        ('KPI', '90-day retention; security adoption; support ticket volume; contract conversion'),
        ('Pilot Duration', '90 days')
    ])
]

for title, items in segments:
    pdf.section_title(title, level=2)
    for label, value in items:
        pdf.bold_bullet(f'{label}: ', value)

pdf.section_title('Cross-Segment Quick Wins (Immediate)', level=2)
pdf.add_table(
    ['Action', 'Effort', 'Impact', 'Timeline'],
    [
        ['Migrate electronic check -> auto-pay', 'Low', 'High', '30 days'],
        ['Enable online security by default', 'Low', 'Medium', '14 days'],
        ['Add risk score to CRM for agents', 'Medium', 'High', '60 days'],
        ['Monthly segment churn dashboard', 'Low', 'Medium', '30 days']
    ],
    col_widths=[60, 20, 20, 30]
)

# ============================================================
# EXPECTED BUSINESS IMPACT
# ============================================================
pdf.add_page()
pdf.section_title('Expected Business Impact')

pdf.section_title('Illustrative Scenario: 10% Relative Churn Reduction Among High-Risk Customers', level=2)

pdf.add_table(
    ['Metric', 'Value', 'Basis'],
    [
        ['High-Risk Customers', '1,833', 'Actual count (Risk_Category = High Risk)'],
        ['Assumed Relative Churn Reduction', '10%', 'Illustrative assumption for scenario planning'],
        ['Estimated Customers Retained', '183', '1,833 x 10%'],
        ['Avg Monthly Charges (High Risk)', '~$85', 'Weighted average from segment data'],
        ['Monthly Revenue Preserved', '~$15,500', '183 x $85'],
        ['Annual Revenue Preserved', '~$186,000', 'Monthly x 12']
    ],
    col_widths=[60, 30, 100]
)

pdf.section_title('Investment vs. Return (Illustrative)', level=2)
pdf.add_table(
    ['Initiative', 'Est. Cost', 'High-Risk Customers', 'Est. Retained (10%)', 'Annual Revenue Saved'],
    [
        ['Senior program', '$150K', '400', '40', '~$350K'],
        ['Budget value plan', '$200K', '750', '75', '~$540K'],
        ['Loyalty program', '$300K', '310', '31', '~$850K'],
        ['Onboarding overhaul', '$100K', '370', '37', '~$270K'],
        ['TOTAL', '$750K', '1,830', '183', '~$2.0M']
    ],
    col_widths=[35, 25, 30, 30, 35]
)

pdf.section_title('Assumptions & Caveats', level=2)
pdf.bullet('Illustrative only - not a forecast or guarantee')
pdf.bullet('Assumes 10% relative uplift on High-Risk churn only (conservative)')
pdf.bullet('Average annual revenue per customer estimated from monthly charges ($700-$1,100 range)')
pdf.bullet('Does not account for implementation costs beyond pilot budget')
pdf.bullet('Requires A/B test validation before any investment decision')
pdf.bullet('External factors (competitors, economy) not modeled')

# ============================================================
# LIMITATIONS
# ============================================================
pdf.add_page()
pdf.section_title('Limitations & Responsible Interpretation')

pdf.add_table(
    ['Limitation', 'Implication'],
    [
        ['Historical data != future behavior', 'Patterns may shift; quarterly refresh essential'],
        ['K-Means encoding sensitivity', 'Label Encoding used; One-Hot tested separately; results may differ'],
        ['Risk score is heuristic', 'Not a predicted probability; no calibration to actual churn likelihood'],
        ['Segments are descriptive', 'Cluster assignments do not predict future segment membership'],
        ['No causal evidence', 'Changing a risk factor (e.g., adding security) may not reduce churn'],
        ['75% overall churn unusually high', 'Validate against current production data before acting'],
        ['Static snapshot', 'Single point-in-time; customer behavior evolves'],
        ['External factors omitted', 'Competitor actions, economic conditions, life events not captured'],
        ['Illustrative impact scenarios', 'Not guaranteed results; require pilot validation']
    ],
    col_widths=[55, 135]
)

pdf.section_title('Responsible Use Guidelines', level=2)
pdf.bullet('Never present risk scores as churn probabilities')
pdf.bullet('Always pair recommendations with pilot validation plans')
pdf.bullet('Segment names are analytical constructs - avoid using them in customer-facing communications')
pdf.bullet('Senior citizen status used analytically - ensure compliance with age discrimination regulations in any outreach')
pdf.bullet('Monitor for unintended consequences - e.g., auto-pay pressure on vulnerable customers')

# ============================================================
# IMPLEMENTATION ROADMAP
# ============================================================
pdf.add_page()
pdf.section_title('Implementation Roadmap')

pdf.add_table(
    ['Phase', 'Timeline', 'Actions', 'Owner'],
    [
        ['Immediate', 'Week 1-2', 'CRM integration of Risk_Score/Risk_Category; support team training', 'IT / Analytics'],
        ['Short-term', 'Month 1', 'Automated daily risk scoring; segment-level dashboards; quick wins launch', 'Analytics / Ops'],
        ['Pilot', 'Quarter 1', 'A/B test retention offers by segment; validate risk score vs 90-day outcomes; calibrate thresholds', 'Analytics / Marketing'],
        ['Scale', 'Ongoing', 'Quarterly segment refresh; expand winning pilots; sunset losers', 'All']
    ],
    col_widths=[25, 25, 90, 25]
)

pdf.section_title('Decisions Required', level=2)
pdf.add_table(
    ['Decision', 'Owner', 'Deadline'],
    [
        ['Approve pilot budget ($750K)', 'VP Retention', 'Dec 1'],
        ['Assign segment ownership', 'Dir. Customer Success', 'Dec 1'],
        ['Integrate risk scores into CRM', 'IT / Analytics', 'Jan 15'],
        ['Design A/B test framework', 'Analytics', 'Jan 15'],
        ['Quarterly refresh schedule', 'Analytics', 'Ongoing']
    ],
    col_widths=[60, 40, 30]
)

# ============================================================
# APPENDIX: REFERENCES
# ============================================================
pdf.add_page()
pdf.section_title('Appendix: Project Assets & References')

assets = [
    ('Interactive Dashboard', 'app.py', 'Run with: streamlit run app.py'),
    ('Segmentation Notebook', 'notebooks/segmentation_and_risk_model_executed.ipynb', 'Executed notebook with outputs'),
    ('EDA Notebook', 'notebooks/analysis.ipynb', 'Exploratory Data Analysis'),
    ('Customer-Level Data', 'data/customer_segmented.csv', '10,000 records with Cluster_ID, Segment_Name, Risk_Score, Risk_Category'),
    ('Segment Summary', 'reports/segment_summary.csv', '4 segments with statistics'),
    ('Detailed Analysis', 'reports/segment_analysis.md', 'Methodology, limitations, findings'),
    ('Recommendation Memo', 'reports/recommendation_memo.md', 'Executive memo with prioritized actions'),
    ('Data Quality Summary', 'reports/data_quality_summary.md', 'Cleaning process documentation'),
    ('Executive Visualizations', 'reports/executive_visualizations/', '12 presentation-ready charts'),
    ('Presentation', 'reports/executive_capstone_presentation.pptx', '11-slide PowerPoint'),
    ('Presentation Script', 'reports/executive_presentation_script.md', 'Speaker notes with timing'),
    ('Metrics Summary', 'reports/executive_metrics_summary.csv', 'Verified metrics with sources'),
]

for name, path, desc in assets:
    pdf.bold_bullet(f'{name}: ', f'{path} - {desc}')

pdf.ln(5)
pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, 'GitHub Repository: [Link to repository - add when available]', 0, 1, 'C')

# Save
output_path = 'reports/executive_capstone_report.pdf'
pdf.output(output_path)
print(f"PDF report saved to {output_path}")
print(f"Pages: {pdf.page_no()}")