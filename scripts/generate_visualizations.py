import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder

sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

DATA_PATH = Path('data/churn_clean.csv')
REPORTS_DIR = Path('reports')
VIS_DIR = REPORTS_DIR / 'segmentation_visualizations'
VIS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Reload customer_segmented to get all columns
df = pd.read_csv('data/customer_segmented.csv')

# Recreate df_prep for PCA
feature_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Contract', 'PaymentMethod',
                'Dependents', 'Partner', 'SeniorCitizen', 'OnlineSecurity']
numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
categorical_features = ['Contract', 'PaymentMethod', 'Dependents', 'Partner', 'OnlineSecurity']

df_prep = df[feature_cols].copy()
label_encoders = {}
for col in categorical_features:
    le = LabelEncoder()
    df_prep[col] = le.fit_transform(df_prep[col].astype(str))
    label_encoders[col] = le

scaler = StandardScaler()
df_prep[numerical_features] = scaler.fit_transform(df_prep[numerical_features])

# ===== VISUALIZATIONS =====

# 1. Customer Segment Distribution
fig, ax = plt.subplots(figsize=(10, 6))
segment_counts = df['Segment_Name'].value_counts().sort_index()
bars = ax.bar(range(len(segment_counts)), segment_counts.values,
              color=sns.color_palette('husl', len(segment_counts)), edgecolor='black')
ax.set_xticks(range(len(segment_counts)))
ax.set_xticklabels(segment_counts.index, rotation=15, ha='right')
ax.set_ylabel('Number of Customers')
ax.set_title('Customer Segment Distribution', fontsize=14, fontweight='bold')
for bar, count in zip(bars, segment_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
            f'{count}', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / 'segment_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# 2. Average Risk Score by Segment
fig, ax = plt.subplots(figsize=(10, 6))
avg_risk = df.groupby('Segment_Name')['Risk_Score'].mean().sort_values()
colors = ['green' if x < 35 else 'orange' if x < 60 else 'red' for x in avg_risk.values]
bars = ax.barh(range(len(avg_risk)), avg_risk.values, color=colors, edgecolor='black')
ax.set_yticks(range(len(avg_risk)))
ax.set_yticklabels(avg_risk.index)
ax.set_xlabel('Average Risk Score')
ax.set_title('Average Risk Score by Segment', fontsize=14, fontweight='bold')
ax.axvline(x=35, color='orange', linestyle='--', alpha=0.5, label='Medium Risk Threshold')
ax.axvline(x=60, color='red', linestyle='--', alpha=0.5, label='High Risk Threshold')
ax.legend()
for bar, val in zip(bars, avg_risk.values):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}', ha='left', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / 'avg_risk_by_segment.png', dpi=150, bbox_inches='tight')
plt.close()

# 3. PCA Visualization
pca = PCA(n_components=2, random_state=42)
pca_result = pca.fit_transform(df_prep)
df['PCA1'] = pca_result[:, 0]
df['PCA2'] = pca_result[:, 1]

fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(df['PCA1'], df['PCA2'], c=df['Cluster_ID'],
                     cmap='tab10', alpha=0.6, s=30)
ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
ax.set_title('Customer Segments (PCA Projection)', fontsize=14, fontweight='bold')
legend1 = ax.legend(*scatter.legend_elements(), title='Cluster ID')
ax.add_artist(legend1)
plt.tight_layout()
plt.savefig(VIS_DIR / 'segmentation_pca.png', dpi=150, bbox_inches='tight')
plt.close()

print(f'PCA Explained Variance: {pca.explained_variance_ratio_.sum():.1%}')

# 4. Risk Category Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

risk_counts = df['Risk_Category'].value_counts()
colors_dict = {'Low Risk': 'green', 'Medium Risk': 'orange', 'High Risk': 'red'}
bars = axes[0].bar(risk_counts.index, risk_counts.values,
                   color=[colors_dict.get(x, 'gray') for x in risk_counts.index], edgecolor='black')
axes[0].set_ylabel('Number of Customers')
axes[0].set_title('Overall Risk Category Distribution', fontsize=13, fontweight='bold')
for bar, count in zip(bars, risk_counts.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                 f'{count} ({count/len(df)*100:.1f}%)', ha='center', va='bottom', fontweight='bold')

risk_by_segment = df.groupby(['Segment_Name', 'Risk_Category']).size().unstack(fill_value=0)
risk_by_segment_pct = risk_by_segment.div(risk_by_segment.sum(axis=1), axis=0) * 100
risk_by_segment_pct.plot(kind='bar', stacked=True, ax=axes[1],
                        color=[colors_dict.get(c, 'gray') for c in risk_by_segment_pct.columns], edgecolor='black')
axes[1].set_ylabel('Percentage')
axes[1].set_title('Risk Category Distribution by Segment', fontsize=13, fontweight='bold')
axes[1].legend(title='Risk Category')
axes[1].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig(VIS_DIR / 'risk_category_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# 5. Comparison of Customer Characteristics Across Segments
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

metrics = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Risk_Score']
titles = ['Tenure (months)', 'Monthly Charges ($)', 'Total Charges ($)', 'Risk Score']

for idx, (metric, title) in enumerate(zip(metrics, titles)):
    ax = axes[idx // 2, idx % 2]
    df.boxplot(column=metric, by='Segment_Name', ax=ax, grid=False)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=15)

plt.suptitle('Customer Characteristics Across Segments', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / 'characteristics_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

# 6. Historical Churn Rate by Segment
fig, ax = plt.subplots(figsize=(10, 6))
churn_by_segment = df.groupby('Segment_Name')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values()
bars = ax.barh(range(len(churn_by_segment)), churn_by_segment.values,
               color=sns.color_palette('RdYlGn_r', len(churn_by_segment)), edgecolor='black')
ax.set_yticks(range(len(churn_by_segment)))
ax.set_yticklabels(churn_by_segment.index)
ax.set_xlabel('Historical Churn Rate (%)')
ax.set_title('Historical Churn Rate by Segment', fontsize=14, fontweight='bold')
for bar, val in zip(bars, churn_by_segment.values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', ha='left', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / 'churn_by_segment.png', dpi=150, bbox_inches='tight')
plt.close()

# 7. Risk Score Distribution: Churned vs Retained
fig, ax = plt.subplots(figsize=(10, 6))
df_churned = df[df['Churn'] == 'Yes']['Risk_Score']
df_retained = df[df['Churn'] == 'No']['Risk_Score']

ax.hist([df_retained, df_churned], bins=30, stacked=True,
        label=['Retained', 'Churned'], color=['green', 'red'], alpha=0.7, edgecolor='black')
ax.set_xlabel('Risk Score')
ax.set_ylabel('Number of Customers')
ax.set_title('Risk Score Distribution: Churned vs Retained Customers', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(VIS_DIR / 'risk_score_churn_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

print("All visualizations saved!")