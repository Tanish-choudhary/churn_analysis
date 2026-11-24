from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# Color palette
COLORS = {
    'primary': RGBColor(0x2C, 0x3E, 0x50),      # Dark blue-gray
    'secondary': RGBColor(0x34, 0x49, 0x5E),    # Medium blue-gray
    'accent': RGBColor(0xE7, 0x4C, 0x3C),       # Red
    'accent_light': RGBColor(0xFA, 0xDB, 0xD8), # Light red
    'success': RGBColor(0x27, 0xAE, 0x60),      # Green
    'warning': RGBColor(0xF3, 0x9C, 0x12),      # Orange
    'info': RGBColor(0x34, 0x98, 0xDB),         # Blue
    'light': RGBColor(0xEC, 0xF0, 0xF1),        # Light gray
    'medium_gray': RGBColor(0xBD, 0xC3, 0xC7),  # Medium gray
    'dark_gray': RGBColor(0x7F, 0x8C, 0x8D),    # Dark gray
    'white': RGBColor(0xFF, 0xFF, 0xFF),
    'dark': RGBColor(0x2C, 0x3E, 0x50),
    'text': RGBColor(0x2C, 0x3E, 0x50),
    'text_light': RGBColor(0x7F, 0x8C, 0x8D),
}

VIS_DIR = 'reports/executive_visualizations'

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape_bg(slide, left, top, width, height, color, transparency=0):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, bold=False, color=None, alignment=PP_ALIGN.LEFT, font_name='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color or COLORS['text']
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_bullet_list(slide, left, top, width, height, items, font_size=16, color=None, spacing=Pt(6), bold_first=False, font_name='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color or COLORS['text']
        p.font.name = font_name
        p.space_after = spacing
        p.level = 0
        if bold_first and ':' in item:
            # We can't easily bold part of a paragraph in python-pptx without runs
            pass
    return txBox

def add_kpi_box(slide, left, top, width, height, label, value, value_color=None, font_name='Calibri'):
    """Add a KPI display box"""
    box = add_shape_bg(slide, left, top, width, height, COLORS['light'])
    add_text_box(slide, left + Inches(0.1), top + Inches(0.05), width - Inches(0.2), Inches(0.4),
                 label, font_size=14, bold=False, color=COLORS['text_light'], alignment=PP_ALIGN.CENTER, font_name=font_name)
    add_text_box(slide, left + Inches(0.1), top + Inches(0.35), width - Inches(0.2), Inches(0.5),
                 value, font_size=28, bold=True, color=value_color or COLORS['primary'], alignment=PP_ALIGN.CENTER, font_name=font_name)

def add_image(slide, image_path, left, top, width=None, height=None):
    """Add image with error handling"""
    if os.path.exists(image_path):
        try:
            if width and height:
                slide.shapes.add_picture(image_path, left, top, width, height)
            elif width:
                slide.shapes.add_picture(image_path, left, top, width=width)
            elif height:
                slide.shapes.add_picture(image_path, left, top, height=height)
            else:
                slide.shapes.add_picture(image_path, left, top)
        except Exception as e:
            print(f"Warning: Could not add image {image_path}: {e}")
    else:
        print(f"Warning: Image not found: {image_path}")

# ============================================================
# SLIDE 1: Title & Business Objective
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
add_background(slide, COLORS['primary'])

# Title area
add_text_box(slide, Inches(1), Inches(1.5), Inches(11), Inches(1.2),
             'Customer Churn Analysis &\nRetention Prioritization', font_size=36, bold=True, color=COLORS['white'], alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1.5), Inches(3.0), Inches(10), Inches(0.8),
             'Executive Analytics Capstone — Executive Presentation', font_size=22, bold=False, color=COLORS['light'], alignment=PP_ALIGN.CENTER)

# Business objective box
obj_box = add_shape_bg(slide, Inches(2), Inches(4.2), Inches(9.3), Inches(1.8), COLORS['secondary'])
add_text_box(slide, Inches(2.3), Inches(4.3), Inches(8.7), Inches(1.6),
             'Business Objective: Identify vulnerable customer segments, prioritize retention resources, and enable data-informed decisions using transparent, explainable analytics — not black-box predictions.',
             font_size=18, bold=False, color=COLORS['light'], alignment=PP_ALIGN.CENTER)

# Footer
add_text_box(slide, Inches(1), Inches(6.5), Inches(11), Inches(0.5),
             'Prepared by: Executive Analytics Capstone Internship Team  |  Date: November 2026', font_size=14, bold=False, color=COLORS['medium_gray'], alignment=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 2: The Business Problem
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

# Header bar
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'The Business Problem: Why Churn Matters', font_size=30, bold=True, color=COLORS['white'])

# Left column - Problem
add_text_box(slide, Inches(0.5), Inches(1.5), Inches(5.5), Inches(0.5),
             'The Cost of Customer Loss', font_size=22, bold=True, color=COLORS['primary'])

problem_items = [
    'Revenue erosion: Every lost customer = lost recurring revenue',
    'Acquisition cost: New customers cost 5-25x more to acquire than retaining existing ones',
    'Competitive risk: Churned customers often switch to competitors',
    'Brand signal: High churn indicates unmet needs or poor experience',
    'Operational impact: Unpredictable revenue makes planning difficult'
]
add_bullet_list(slide, Inches(0.5), Inches(2.2), Inches(5.5), Inches(3.5), problem_items, font_size=16, color=COLORS['text'])

# Right column - Business Question
add_shape_bg(slide, Inches(7), Inches(1.5), Inches(5.8), Inches(4.5), COLORS['light'])
add_text_box(slide, Inches(7.3), Inches(1.7), Inches(5.2), Inches(0.5),
             'Key Business Questions', font_size=22, bold=True, color=COLORS['primary'])

questions = [
    'Which customers are most likely to leave?',
    'What characteristics define vulnerable segments?',
    'Where should we focus limited retention resources?',
    'What actions address the root risk factors?',
    'How do we measure the impact of interventions?'
]
add_bullet_list(slide, Inches(7.3), Inches(2.4), Inches(5.2), Inches(3.5), questions, font_size=16, color=COLORS['text'], spacing=Pt(10))

# Bottom insight box
add_shape_bg(slide, Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.8), COLORS['accent_light'])
add_text_box(slide, Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.6),
             '⚠ Without prioritization, retention efforts are spread too thin — high-value and high-risk customers receive the same attention as low-risk ones.',
             font_size=15, bold=True, color=COLORS['accent'], alignment=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 3: Data Quality & Analytical Foundation
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'Data Quality & Analytical Foundation', font_size=30, bold=True, color=COLORS['white'])

# KPI row
add_kpi_box(slide, Inches(0.5), Inches(1.5), Inches(2.8), Inches(1.2), 'Total Customers', '10,000', COLORS['primary'])
add_kpi_box(slide, Inches(3.6), Inches(1.5), Inches(2.8), Inches(1.2), 'Overall Churn Rate', '75.06%', COLORS['accent'])
add_kpi_box(slide, Inches(6.7), Inches(1.5), Inches(2.8), Inches(1.2), 'Retention Rate', '24.94%', COLORS['warning'])
add_kpi_box(slide, Inches(9.8), Inches(1.5), Inches(2.8), Inches(1.2), 'Monthly Revenue', '$688,744', COLORS['success'])

# Data quality section
add_text_box(slide, Inches(0.5), Inches(3.0), Inches(6), Inches(0.5),
             'Data Quality Process', font_size=22, bold=True, color=COLORS['primary'])

dq_items = [
    'Raw dataset: 10,100 records → 10,000 clean records after deduplication',
    'Missing values: Imputed using median (charges) and mode (categorical)',
    'Data types: Standardized — numeric charges, categorical labels cleaned',
    'Outliers: Flagged via IQR method, preserved for transparency',
    'Logical consistency: TotalCharges validated against tenure × monthly charges'
]
add_bullet_list(slide, Inches(0.5), Inches(3.6), Inches(6), Inches(2.5), dq_items, font_size=15, color=COLORS['text'])

# Analytical approach
add_text_box(slide, Inches(7), Inches(3.0), Inches(5.8), Inches(0.5),
             'Analytical Approach', font_size=22, bold=True, color=COLORS['primary'])

approach_items = [
    '1. Exploratory Analysis: Churn patterns by contract, tenure, services',
    '2. Business KPI Dashboard: Interactive monitoring & filtering',
    '3. Customer Segmentation: K-Means clustering (4 segments, no Churn leakage)',
    '4. Rule-Based Risk Scoring: Transparent 0-100 score (7 factors, no ML black box)',
    '5. Segment Evaluation: Historical churn rates used only for validation'
]
add_bullet_list(slide, Inches(7), Inches(3.6), Inches(5.8), Inches(2.5), approach_items, font_size=15, color=COLORS['text'], spacing=Pt(8))

# Key principle box
add_shape_bg(slide, Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.8), COLORS['info'])
add_text_box(slide, Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.6),
             'Principle: No Churn data used to create segments or risk scores — only to validate results afterward.',
             font_size=15, bold=True, color=COLORS['white'], alignment=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 4: Key Findings from Exploratory Analysis
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'Key Findings: What Drives Churn?', font_size=30, bold=True, color=COLORS['white'])

# Add visualizations
add_image(slide, f'{VIS_DIR}/churn_by_contract.png', Inches(0.3), Inches(1.3), width=Inches(6.2))
add_image(slide, f'{VIS_DIR}/churn_by_tenure.png', Inches(6.8), Inches(1.3), width=Inches(6.2))

# Findings summary
add_shape_bg(slide, Inches(0.5), Inches(5.0), Inches(12.3), Inches(2.0), COLORS['light'])
add_text_box(slide, Inches(0.8), Inches(5.1), Inches(11.7), Inches(0.4),
             'Validated Patterns from 10,000 Customers', font_size=20, bold=True, color=COLORS['primary'])

findings = [
    'Contract type: Month-to-month customers churn at 74.7% vs 75.5% (Two year) — minimal difference, all high',
    'Tenure effect: Lowest quartile (0-12 mo) churns at 75.9%; highest (50+ mo) at 76.8% — tenure alone not protective',
    'Payment method: Electronic check users show higher risk; auto-pay associated with stability',
    'Service gaps: Customers without online security have elevated risk scores',
    'Senior citizens: 100% of Senior Vulnerable segment are seniors — unique risk profile'
]
add_bullet_list(slide, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.5), findings, font_size=14, color=COLORS['text'], spacing=Pt(4))

# ============================================================
# SLIDE 5: Business KPI Dashboard
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'Business KPI Dashboard: Live Monitoring', font_size=30, bold=True, color=COLORS['white'])

# Dashboard screenshot placeholder
add_shape_bg(slide, Inches(0.5), Inches(1.4), Inches(8), Inches(4.5), COLORS['light'])
add_text_box(slide, Inches(0.8), Inches(3.2), Inches(7.4), Inches(1.0),
             '[Interactive Streamlit Dashboard Screenshot]\nRun: streamlit run app.py', font_size=18, bold=False, color=COLORS['text_light'], alignment=PP_ALIGN.CENTER)

# KPIs from dashboard
add_text_box(slide, Inches(9), Inches(1.5), Inches(4), Inches(0.4),
             'Dashboard KPIs', font_size=22, bold=True, color=COLORS['primary'])

add_kpi_box(slide, Inches(9), Inches(2.2), Inches(3.8), Inches(1.0), 'Overall Churn Rate', '75.06%', COLORS['accent'])
add_kpi_box(slide, Inches(9), Inches(3.4), Inches(3.8), Inches(1.0), 'Retention Rate', '24.94%', COLORS['warning'])
add_kpi_box(slide, Inches(9), Inches(4.6), Inches(3.8), Inches(1.0), 'Monthly Rev. at Risk (High Risk)', '$155,849', COLORS['accent'])

# Features
add_text_box(slide, Inches(0.5), Inches(6.1), Inches(12.3), Inches(0.3),
             'Dashboard Features', font_size=18, bold=True, color=COLORS['primary'])

features = [
    'Interactive filters: Contract type, Tenure range, Monthly charges',
    'Real-time KPI updates as filters change',
    'Visualizations: Churn by contract, tenure distribution, revenue at risk, customer segmentation',
    'Auto-generated business insights based on filtered view'
]
add_bullet_list(slide, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.8), features, font_size=14, color=COLORS['text'], spacing=Pt(2))

# ============================================================
# SLIDE 6: Customer Segmentation
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'Customer Segmentation: Four Distinct Groups', font_size=30, bold=True, color=COLORS['white'])

# Segment distribution chart
add_image(slide, f'{VIS_DIR}/segment_distribution.png', Inches(0.3), Inches(1.3), width=Inches(6.2))

# Segment radar
add_image(slide, f'{VIS_DIR}/segment_radar.png', Inches(6.8), Inches(1.3), width=Inches(6.2))

# Segment details table
add_text_box(slide, Inches(0.5), Inches(4.6), Inches(12), Inches(0.4),
             'Segment Profiles (Verified from Data)', font_size=20, bold=True, color=COLORS['primary'])

segments_data = [
    ['Senior Vulnerable', '1,546 (15.5%)', '75.0%', '$67.17', '34.7 mo', '47.0', '25.9%'],
    ['Budget-Conscious', '3,151 (31.5%)', '75.3%', '$59.49', '28.8 mo', '45.1', '23.9%'],
    ['High-Value Long-Term', '2,343 (23.4%)', '76.2%', '$91.76', '56.2 mo', '41.6', '13.2%'],
    ['New Vulnerable', '2,960 (29.6%)', '74.0%', '$61.64', '28.4 mo', '38.2', '12.6%']
]

# Create table
from pptx.util import Inches, Pt
table_shape = slide.shapes.add_table(5, 7, Inches(0.5), Inches(5.1), Inches(12.3), Inches(2.2))
table = table_shape.table

headers = ['Segment', 'Customers', 'Hist. Churn', 'Avg Monthly', 'Avg Tenure', 'Avg Risk', '% High Risk']
for i, h in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = h
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.size = Pt(12)
        paragraph.font.bold = True
        paragraph.font.color.rgb = COLORS['white']
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLORS['primary']

segment_colors_list = [COLORS['accent'], COLORS['warning'], COLORS['success'], COLORS['info']]
for row_idx, row_data in enumerate(segments_data):
    for col_idx, val in enumerate(row_data):
        cell = table.cell(row_idx + 1, col_idx)
        cell.text = val
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(11)
            paragraph.font.color.rgb = COLORS['text']
        if row_idx % 2 == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLORS['light']

# ============================================================
# SLIDE 7: Risk Prioritization
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'Risk Prioritization: Transparent Rule-Based Scoring', font_size=30, bold=True, color=COLORS['white'])

# Risk category distribution
add_image(slide, f'{VIS_DIR}/risk_category_distribution.png', Inches(0.3), Inches(1.3), width=Inches(5.5))

# Risk score by segment
add_image(slide, f'{VIS_DIR}/risk_score_by_segment.png', Inches(6.3), Inches(1.3), width=Inches(6.5))

# Risk scoring explanation
add_shape_bg(slide, Inches(0.5), Inches(4.6), Inches(12.3), Inches(2.5), COLORS['light'])
add_text_box(slide, Inches(0.8), Inches(4.7), Inches(11.7), Inches(0.4),
             'How the Risk Score Works (0-100)', font_size=20, bold=True, color=COLORS['primary'])

score_factors = [
    'Short tenure (≤6 mo): +25 pts  |  High monthly charges (≥$90): +20 pts  |  Month-to-month contract: +25 pts',
    'Electronic check payment: +10 pts  |  No online security: +10 pts  |  Senior citizen: +5 pts  |  No partner/dependents: +5 pts',
    'Maximum possible: 100  |  Low Risk: 0-34  |  Medium Risk: 35-59  |  High Risk: 60-100',
    '⚠ This is a prioritization heuristic, NOT a predicted probability of churn.'
]
add_bullet_list(slide, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.8), score_factors, font_size=14, color=COLORS['text'], spacing=Pt(4))

# Key stats
add_text_box(slide, Inches(0.5), Inches(6.3), Inches(12.3), Inches(0.3),
             'Risk Distribution: 2,793 Low (27.9%)  |  5,374 Medium (53.7%)  |  1,833 High (18.3%)  |  High Risk Monthly Revenue: $155,849',
             font_size=15, bold=True, color=COLORS['primary'], alignment=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 8: Segment-Specific Recommendations
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'Segment-Specific Recommendations', font_size=30, bold=True, color=COLORS['white'])

# Four recommendation boxes
segments_recs = [
    ('Senior Vulnerable\n(Priority 1)', COLORS['accent'], [
        'Dedicated senior support line with trained agents',
        'Contract upgrade incentive: 20% off first year annual',
        'Auto-pay migration assistance (electronic check → auto-pay)',
        'Free online security bundle with contract upgrade',
        'Quarterly proactive check-in calls for High Risk'
    ]),
    ('Budget-Conscious\n(Priority 2)', COLORS['warning'], [
        'Launch "Essentials" value tier at ~$45/month',
        'Annual commitment discount: 15% off (effective ~$50.60)',
        'Auto-pay nudge campaign with $5/mo credit incentive',
        'Usage alerts to prevent bill shock'
    ]),
    ('High-Value Long-Term\n(Priority 3)', COLORS['success'], [
        'Tiered loyalty program (Silver/Gold/Platinum by tenure)',
        'Price protection guarantee: lock rate for 24 months',
        'Dedicated account manager for top 20%',
        'Premium security suite + device upgrade every 24 mo',
        'Win-back protocol with authorized retention offers'
    ]),
    ('New Vulnerable\n(Priority 4)', COLORS['info'], [
        'Structured 30/60/90 day onboarding journey',
        'Default-on online security (opt-out model)',
        'First-year contract incentive: auto-convert at month 4',
        'Early warning system: >2 tickets in 90 days = outreach'
    ])
]

for i, (title, color, recs) in enumerate(segments_recs):
    x = Inches(0.3 + i * 3.25)
    y = Inches(1.4)
    w = Inches(3.1)
    h = Inches(5.5)

    box = add_shape_bg(slide, x, y, w, h, COLORS['light'])
    # Title bar
    add_shape_bg(slide, x, y, w, Inches(0.7), color)
    add_text_box(slide, x + Inches(0.1), y + Inches(0.05), w - Inches(0.2), Inches(0.6),
                 title, font_size=15, bold=True, color=COLORS['white'], alignment=PP_ALIGN.CENTER)

    # Recommendations
    rec_items = [f'• {r}' for r in recs]
    add_bullet_list(slide, x + Inches(0.15), y + Inches(0.85), w - Inches(0.3), h - Inches(1.0),
                    rec_items, font_size=12, color=COLORS['text'], spacing=Pt(4))

# ============================================================
# SLIDE 9: Expected Business Impact
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'Expected Business Impact: Illustrative Scenario', font_size=30, bold=True, color=COLORS['white'])

# Impact scenario chart
add_image(slide, f'{VIS_DIR}/impact_scenario.png', Inches(0.3), Inches(1.3), width=Inches(8.5))

# Calculation details
add_shape_bg(slide, Inches(9), Inches(1.3), Inches(3.8), Inches(4.5), COLORS['light'])
add_text_box(slide, Inches(9.2), Inches(1.5), Inches(3.4), Inches(0.4),
             'Illustrative Calculation', font_size=18, bold=True, color=COLORS['primary'])

calc_items = [
    'Target: High-Risk customers (1,833)',
    'Assumption: 10% relative churn reduction',
    '= 183 customers retained',
    '',
    'Avg monthly charges (High Risk): ~$85',
    'Monthly revenue preserved: ~$15,500',
    'Annual revenue preserved: ~$186,000',
    '',
    'Investment estimate: $750K (4 pilots)',
    'Illustrative ROI: ~4x in Year 1',
    '',
    '⚠ Assumes 10% uplift on High Risk only',
    '⚠ Not a guarantee — requires pilot validation'
]
add_bullet_list(slide, Inches(9.2), Inches(2.0), Inches(3.4), Inches(3.5), calc_items, font_size=12, color=COLORS['text'], spacing=Pt(2))

# Current metrics box
add_shape_bg(slide, Inches(0.5), Inches(5.5), Inches(12.3), Inches(1.5), COLORS['accent_light'])
add_text_box(slide, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.3),
             'Current Baseline (Verified):\n• 10,000 customers  • 75.06% historical churn  • $688,744 monthly revenue  • 1,833 High Risk ($155,849/mo at risk)\n• This scenario assumes 10% relative reduction ONLY among High Risk — conservative, not a forecast.',
             font_size=14, bold=False, color=COLORS['accent'], alignment=PP_ALIGN.LEFT)

# ============================================================
# SLIDE 10: Implementation Roadmap & Limitations
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['white'])

add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.1), COLORS['primary'])
add_text_box(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
             'Implementation Roadmap & Limitations', font_size=30, bold=True, color=COLORS['white'])

# Roadmap
add_image(slide, f'{VIS_DIR}/roadmap.png', Inches(0.3), Inches(1.3), width=Inches(7.5))

# Limitations
add_shape_bg(slide, Inches(8.2), Inches(1.3), Inches(4.8), Inches(5.5), COLORS['light'])
add_text_box(slide, Inches(8.5), Inches(1.5), Inches(4.2), Inches(0.4),
             'Limitations & Responsible Use', font_size=20, bold=True, color=COLORS['primary'])

limitations = [
    'Historical data ≠ future behavior',
    'K-Means sensitive to encoding (Label vs One-Hot)',
    'Risk score is heuristic, not ML probability',
    'Segments are descriptive, not predictive',
    'No causal evidence: changing a factor may not reduce churn',
    '75% overall churn unusually high — validate on current data',
    'Static snapshot — refresh quarterly',
    'External factors not captured (competitors, economy)',
    'Pilot validation required before scaling'
]
add_bullet_list(slide, Inches(8.5), Inches(2.1), Inches(4.2), Inches(4.5), limitations, font_size=13, color=COLORS['text'], spacing=Pt(3))

# Next steps
add_text_box(slide, Inches(0.5), Inches(6.3), Inches(7.5), Inches(0.3),
             'Immediate Next Steps (30 Days)', font_size=18, bold=True, color=COLORS['primary'])

next_steps = [
    'Integrate Risk_Score & Risk_Category into CRM',
    'Train support teams on risk factor explanations',
    'Launch Quick Wins: Auto-pay migration, Security default-on',
    'Design A/B test framework for Priority 1 segment'
]
add_bullet_list(slide, Inches(0.5), Inches(6.7), Inches(7.5), Inches(0.7), next_steps, font_size=14, color=COLORS['text'], spacing=Pt(2))

# ============================================================
# SLIDE 11: Conclusion
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLORS['primary'])

add_text_box(slide, Inches(1), Inches(1.0), Inches(11), Inches(1.0),
             'Three Key Takeaways', font_size=36, bold=True, color=COLORS['white'], alignment=PP_ALIGN.CENTER)

takeaways = [
    ('1', 'Churn is pervasive (75%) but not uniform — four segments have distinct risk profiles requiring different actions'),
    ('2', 'Transparent rule-based scoring enables immediate prioritization without black-box models'),
    ('3', 'Targeted pilots on High-Risk segments can demonstrate ROI before full-scale investment')
]

for i, (num, text) in enumerate(takeaways):
    y = Inches(2.5 + i * 1.3)
    add_shape_bg(slide, Inches(2), y, Inches(1.2), Inches(1.2), COLORS['accent'])
    add_text_box(slide, Inches(2), y + Inches(0.2), Inches(1.2), Inches(0.8),
                 num, font_size=48, bold=True, color=COLORS['white'], alignment=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(3.5), y + Inches(0.2), Inches(8), Inches(0.8),
                 text, font_size=20, bold=False, color=COLORS['white'], alignment=PP_ALIGN.LEFT)

# Decision box
add_shape_bg(slide, Inches(1.5), Inches(6.2), Inches(10.3), Inches(0.8), COLORS['accent'])
add_text_box(slide, Inches(1.8), Inches(6.3), Inches(9.7), Inches(0.6),
             'Decision Requested: Approve $750K pilot budget for 90-day segment-specific retention programs with A/B testing',
             font_size=20, bold=True, color=COLORS['white'], alignment=PP_ALIGN.CENTER)

# Save
output_path = 'reports/executive_capstone_presentation.pptx'
prs.save(output_path)
print(f"Presentation saved to {output_path}")
print(f"Slides: {len(prs.slides)}")