import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Professional color palette
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#34495E',
    'accent': '#E74C3C',
    'accent_light': '#FADBD8',
    'success': '#27AE60',
    'warning': '#F39C12',
    'info': '#3498DB',
    'light_gray': '#ECF0F1',
    'medium_gray': '#BDC3C7',
    'dark_gray': '#7F8C8D',
    'segment_colors': {
        'Senior Vulnerable Customers': '#E74C3C',
        'Budget-Conscious Customers': '#F39C12',
        'High-Value Long-Term Customers': '#27AE60',
        'New Vulnerable Customers': '#3498DB'
    },
    'risk_colors': {
        'Low Risk': '#27AE60',
        'Medium Risk': '#F39C12',
        'High Risk': '#E74C3C'
    }
}

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# Paths
DATA_PATH = Path('data/churn_clean.csv')
SEG_PATH = Path('data/customer_segmented.csv')
SUMMARY_PATH = Path('reports/segment_summary.csv')
VIS_DIR = Path('reports/executive_visualizations')
VIS_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)
df_seg = pd.read_csv(SEG_PATH)
summary = pd.read_csv(SUMMARY_PATH)

# ============================================================
# CHART 1: Overall KPIs - Churn vs Retention
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5))
churn_rate = (df['Churn'] == 'Yes').mean() * 100
retention_rate = 100 - churn_rate

wedges, texts, autotexts = ax.pie(
    [retention_rate, churn_rate],
    labels=['Retained', 'Churned'],
    colors=[COLORS['success'], COLORS['accent']],
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(13)

ax.set_title('Overall Customer Churn vs Retention', fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(VIS_DIR / 'kpi_churn_retention.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 2: Monthly Revenue at Risk
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
total_monthly = df_seg['MonthlyCharges'].sum()
high_risk_monthly = df_seg[df_seg['Risk_Category'] == 'High Risk']['MonthlyCharges'].sum()
medium_risk_monthly = df_seg[df_seg['Risk_Category'] == 'Medium Risk']['MonthlyCharges'].sum()
low_risk_monthly = df_seg[df_seg['Risk_Category'] == 'Low Risk']['MonthlyCharges'].sum()

categories = ['Low Risk', 'Medium Risk', 'High Risk']
values = [low_risk_monthly, medium_risk_monthly, high_risk_monthly]
colors = [COLORS['risk_colors'][c] for c in categories]

bars = ax.barh(categories, values, color=colors, edgecolor='white', height=0.6)
ax.set_xlabel('Monthly Recurring Revenue ($)', fontweight='bold')
ax.set_title('Monthly Revenue by Risk Category', fontweight='bold', pad=15)

for bar, val in zip(bars, values):
    ax.text(bar.get_width() + 5000, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontweight='bold', fontsize=11)

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))
ax.set_xlim(0, max(values) * 1.25)
plt.tight_layout()
plt.savefig(VIS_DIR / 'revenue_by_risk.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 3: Segment Distribution
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
segment_order = summary.sort_values('Customer_Count', ascending=True)['Segment_Name'].tolist()
counts = summary.set_index('Segment_Name').loc[segment_order, 'Customer_Count']
colors = [COLORS['segment_colors'][s] for s in segment_order]

bars = ax.barh(segment_order, counts, color=colors, edgecolor='white', height=0.6)
ax.set_xlabel('Number of Customers', fontweight='bold')
ax.set_title('Customer Segment Distribution', fontweight='bold', pad=15)

for bar, val in zip(bars, counts):
    pct = val / len(df_seg) * 100
    ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2,
            f'{val:,} ({pct:.1f}%)', va='center', fontweight='bold', fontsize=11)

ax.set_xlim(0, max(counts) * 1.2)
plt.tight_layout()
plt.savefig(VIS_DIR / 'segment_distribution.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 4: Historical Churn Rate by Segment
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
churn_rates = summary.set_index('Segment_Name').loc[segment_order, 'Historical_Churn_Rate']
colors = [COLORS['segment_colors'][s] for s in segment_order]

bars = ax.barh(segment_order, churn_rates, color=colors, edgecolor='white', height=0.6, alpha=0.85)
ax.set_xlabel('Historical Churn Rate (%)', fontweight='bold')
ax.set_title('Historical Churn Rate by Segment', fontweight='bold', pad=15)

for bar, val in zip(bars, churn_rates):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', fontweight='bold', fontsize=11)

ax.axvline(x=churn_rate, color=COLORS['dark_gray'], linestyle='--', alpha=0.6, label=f'Overall: {churn_rate:.1f}%')
ax.legend(loc='lower right', fontsize=10)
ax.set_xlim(0, max(churn_rates) * 1.15)
plt.tight_layout()
plt.savefig(VIS_DIR / 'churn_by_segment.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 5: Risk Score Distribution by Segment
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
risk_scores = summary.set_index('Segment_Name').loc[segment_order, 'Avg_Risk_Score']
colors = [COLORS['segment_colors'][s] for s in segment_order]

bars = ax.barh(segment_order, risk_scores, color=colors, edgecolor='white', height=0.6)
ax.set_xlabel('Average Risk Score (0-100)', fontweight='bold')
ax.set_title('Average Rule-Based Risk Score by Segment', fontweight='bold', pad=15)

# Add threshold lines
ax.axvline(x=35, color=COLORS['warning'], linestyle='--', alpha=0.5, label='Medium Risk Threshold (35)')
ax.axvline(x=60, color=COLORS['accent'], linestyle='--', alpha=0.5, label='High Risk Threshold (60)')

for bar, val in zip(bars, risk_scores):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}', va='center', fontweight='bold', fontsize=11)

ax.legend(loc='lower right', fontsize=9)
ax.set_xlim(0, 70)
plt.tight_layout()
plt.savefig(VIS_DIR / 'risk_score_by_segment.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 6: Risk Category Distribution
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5))
risk_dist = df_seg['Risk_Category'].value_counts()
# Ensure order: Low, Medium, High
risk_order = ['Low Risk', 'Medium Risk', 'High Risk']
risk_counts = [risk_dist.get(c, 0) for c in risk_order]
risk_pcts = [c / len(df_seg) * 100 for c in risk_counts]
colors = [COLORS['risk_colors'][c] for c in risk_order]

wedges, texts = ax.pie(
    risk_counts,
    labels=None,
    colors=colors,
    autopct=None,
    startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)

# Custom legend with counts and percentages
legend_labels = [f'{c}: {cnt:,} ({pct:.1f}%)' for c, cnt, pct in zip(risk_order, risk_counts, risk_pcts)]
ax.legend(wedges, legend_labels, title='Risk Category', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
ax.set_title('Customer Risk Category Distribution', fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(VIS_DIR / 'risk_category_distribution.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 7: Churn by Contract Type
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
contract_data = df_seg.groupby('Contract').agg(
    churn_rate=('Churn', lambda x: (x == 'Yes').mean() * 100),
    count=('Churn', 'count')
).sort_values('churn_rate', ascending=True)

colors = [COLORS['info'], COLORS['warning'], COLORS['accent']][:len(contract_data)]
bars = ax.barh(contract_data.index, contract_data['churn_rate'], color=colors, edgecolor='white', height=0.6)
ax.set_xlabel('Churn Rate (%)', fontweight='bold')
ax.set_title('Churn Rate by Contract Type', fontweight='bold', pad=15)

for bar, (idx, row) in zip(bars, contract_data.iterrows()):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{row["churn_rate"]:.1f}% (n={row["count"]:,})', va='center', fontweight='bold', fontsize=10)

ax.axvline(x=churn_rate, color=COLORS['dark_gray'], linestyle='--', alpha=0.6, label=f'Overall: {churn_rate:.1f}%')
ax.legend(loc='lower right', fontsize=9)
ax.set_xlim(0, max(contract_data['churn_rate']) * 1.15)
plt.tight_layout()
plt.savefig(VIS_DIR / 'churn_by_contract.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 8: Churn by Tenure Quartile
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
df_seg['tenure_quartile'] = pd.qcut(df_seg['tenure'], q=4, labels=['Q1 (0-12 mo)', 'Q2 (12-28 mo)', 'Q3 (28-50 mo)', 'Q4 (50+ mo)'])
tenure_churn = df_seg.groupby('tenure_quartile')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).reset_index()
tenure_counts = df_seg['tenure_quartile'].value_counts().sort_index().reset_index()
tenure_counts.columns = ['tenure_quartile', 'count']

merged = tenure_churn.merge(tenure_counts, on='tenure_quartile')

colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(merged)))
bars = ax.bar(merged['tenure_quartile'], merged['Churn'], color=colors, edgecolor='white')
ax.set_ylabel('Churn Rate (%)', fontweight='bold')
ax.set_xlabel('Tenure Quartile', fontweight='bold')
ax.set_title('Churn Rate by Tenure Quartile', fontweight='bold', pad=15)

for bar, (_, row) in zip(bars, merged.iterrows()):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{row["Churn"]:.1f}%\n(n={row["count"]:,})', ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.axhline(y=churn_rate, color=COLORS['dark_gray'], linestyle='--', alpha=0.6, label=f'Overall: {churn_rate:.1f}%')
ax.legend(loc='upper right', fontsize=9)
ax.set_ylim(0, max(merged['Churn']) * 1.15)
plt.tight_layout()
plt.savefig(VIS_DIR / 'churn_by_tenure.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 9: Segment Profile Radar - Key Metrics
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))

# Normalize metrics for comparison
metrics = ['Avg_Tenure', 'Avg_Monthly_Charges', 'Avg_Risk_Score', 'Historical_Churn_Rate', 'Pct_High_Risk']
labels = ['Tenure\n(months)', 'Monthly\nCharges ($)', 'Risk\nScore (0-100)', 'Churn\nRate (%)', '% High\nRisk']

# Normalize each metric to 0-1 scale for radar
norm_data = {}
for metric in metrics:
    vals = summary[metric].values
    norm_data[metric] = (vals - vals.min()) / (vals.max() - vals.min()) if vals.max() != vals.min() else np.zeros(len(vals))

angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]  # Close the loop

# Set up the plot
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=10)
ax.set_yticks([0, 0.5, 1.0])
ax.set_yticklabels(['Min', 'Med', 'Max'], fontsize=9)

# Get segment order
seg_names = summary['Segment_Name'].tolist()

for i, name in enumerate(seg_names):
    color = COLORS['segment_colors'][name]
    idx = summary[summary['Segment_Name'] == name].index[0]
    values = [norm_data[m][idx] for m in metrics]
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=name, color=color)
    ax.fill(angles, values, alpha=0.1, color=color)

ax.set_title('Segment Profile Comparison (Normalized Metrics)', fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
plt.tight_layout()
plt.savefig(VIS_DIR / 'segment_radar.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 10: Expected Impact Scenario - Illustrative
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))

# Scenario: 10% relative churn reduction on High Risk customers
segments = ['Senior Vulnerable Customers', 'Budget-Conscious Customers', 'High-Value Long-Term Customers', 'New Vulnerable Customers']
high_risk_counts = summary.set_index('Segment_Name').loc[segments, 'Pct_High_Risk'] / 100 * summary.set_index('Segment_Name').loc[segments, 'Customer_Count']
avg_monthly = summary.set_index('Segment_Name').loc[segments, 'Avg_Monthly_Charges']

# Current monthly revenue at risk from High Risk
current_at_risk = (high_risk_counts * avg_monthly).sum()

# Illustrative: 10% relative reduction in churn among High Risk
# = 10% of High Risk customers retained
retained_10pct = high_risk_counts * 0.10
revenue_saved_monthly = (retained_10pct * avg_monthly).sum()
revenue_saved_annual = revenue_saved_monthly * 12

x = np.arange(len(segments))
width = 0.35

bars1 = ax.bar(x - width/2, high_risk_counts, width, label='High Risk Customers', color=COLORS['accent'], alpha=0.7, edgecolor='white')
bars2 = ax.bar(x + width/2, retained_10pct, width, label='Illustrative Retained (10% of High Risk)', color=COLORS['success'], alpha=0.7, edgecolor='white')

ax.set_ylabel('Number of Customers', fontweight='bold')
ax.set_title('Illustrative Impact: 10% Relative Churn Reduction Among High-Risk Customers', fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(segments, rotation=15, ha='right')
ax.legend()

# Add value labels
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{bar.get_height():.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{bar.get_height():.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

# Add revenue annotation
ax.text(0.98, 0.95, f'Monthly Revenue Saved: ${revenue_saved_monthly:,.0f}\nAnnual Revenue Saved: ${revenue_saved_annual:,.0f}',
        transform=ax.transAxes, ha='right', va='top', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['light_gray'], edgecolor=COLORS['dark_gray']))

plt.tight_layout()
plt.savefig(VIS_DIR / 'impact_scenario.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 11: Monthly Revenue by Segment
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
seg_revenue = summary.set_index('Segment_Name').loc[segment_order]
monthly_revenue = seg_revenue['Customer_Count'] * seg_revenue['Avg_Monthly_Charges']
colors = [COLORS['segment_colors'][s] for s in segment_order]

bars = ax.barh(segment_order, monthly_revenue, color=colors, edgecolor='white', height=0.6)
ax.set_xlabel('Monthly Recurring Revenue ($)', fontweight='bold')
ax.set_title('Monthly Revenue Contribution by Segment', fontweight='bold', pad=15)

for bar, val in zip(bars, monthly_revenue):
    ax.text(bar.get_width() + 5000, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontweight='bold', fontsize=11)

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))
ax.set_xlim(0, max(monthly_revenue) * 1.2)
plt.tight_layout()
plt.savefig(VIS_DIR / 'revenue_by_segment.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 12: Implementation Roadmap Timeline
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))

phases = [
    ('Week 1-2', 'CRM Integration\nRisk Score Training', COLORS['info']),
    ('Month 1', 'Auto Risk Scoring\nSegment Dashboards', COLORS['warning']),
    ('Quarter 1', 'A/B Test Retention\nValidate & Calibrate', COLORS['success']),
    ('Ongoing', 'Quarterly Refresh\nScale Winners', COLORS['primary'])
]

y_pos = np.arange(len(phases))
colors = [p[2] for p in phases]

bars = ax.barh(y_pos, [1]*len(phases), left=0, height=0.6, color=colors, edgecolor='white', alpha=0.8)

for i, (period, desc, _) in enumerate(phases):
    ax.text(0.02, i, f'{period}', va='center', ha='left', fontweight='bold', fontsize=11, color='white')
    ax.text(0.35, i, desc, va='center', ha='left', fontsize=10, color=COLORS['dark_gray'])

ax.set_xlim(0, 1)
ax.set_yticks([])
ax.set_title('Implementation Roadmap', fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.get_xaxis().set_visible(False)

plt.tight_layout()
plt.savefig(VIS_DIR / 'roadmap.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

print("All executive visualizations created successfully!")
print(f"Saved to: {VIS_DIR}")
print("Files:")
for f in sorted(VIS_DIR.glob('*.png')):
    print(f"  - {f.name}")