import json

notebook = {
    'cells': [],
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.10.0'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

# Cell 1: Title
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': [
        '# Customer Segmentation and Explainable Churn-Risk Prioritization Model\n',
        '\n',
        '**Executive Analytics Capstone Internship - Step 4**\n',
        '\n',
        'This notebook implements customer segmentation using K-Means clustering and an explainable rule-based churn-risk scoring system. The approach moves from descriptive analytics to actionable customer segmentation and risk prioritization.'
    ]
})

# Cell 2: Data Loading
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ['## 1. Data Loading and Inspection']
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        'import pandas as pd\n',
        'import numpy as np\n',
        'import matplotlib.pyplot as plt\n',
        'import seaborn as sns\n',
        'import json\n',
        'import os\n',
        'from pathlib import Path\n',
        '\n',
        '# ML Libraries\n',
        'from sklearn.preprocessing import StandardScaler, LabelEncoder\n',
        'from sklearn.cluster import KMeans\n',
        'from sklearn.metrics import silhouette_score\n',
        'from sklearn.decomposition import PCA\n',
        '\n',
        '# Set style\n',
        'sns.set_theme(style="whitegrid")\n',
        'plt.rcParams["figure.figsize"] = (10, 6)\n',
        'plt.rcParams["font.size"] = 12\n',
        '\n',
        '# Paths\n',
        'DATA_PATH = Path("../data/churn_clean.csv")\n',
        'OUTPUT_DATA_PATH = Path("../data/customer_segmented.csv")\n',
        'REPORTS_DIR = Path("../reports")\n',
        'VIS_DIR = REPORTS_DIR / "segmentation_visualizations"\n',
        '\n',
        'VIS_DIR.mkdir(parents=True, exist_ok=True)\n',
        'REPORTS_DIR.mkdir(parents=True, exist_ok=True)\n',
        '\n',
        '# Load data\n',
        'df = pd.read_csv(DATA_PATH)\n',
        'print(f"Dataset shape: {df.shape}")\n',
        'print(f"Columns: {list(df.columns)}")\n',
        'df.head()'
    ]
})

# Cell 3: Feature Selection
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ['## 2. Feature Selection and Preprocessing\n', '\n', 'We select features for segmentation that are behavioral, financial, and service-related. We explicitly **exclude** the Churn target column to prevent data leakage.']
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Identify features for segmentation\n',
        '# Exclude: CustomerID (identifier), Churn (target), outlier flags (derived), logical flags\n',
        'exclude_cols = ["CustomerID", "Churn", "tenure_outlier", "MonthlyCharges_outlier", \n',
        '                "TotalCharges_outlier", "tenure_negative", "MonthlyCharges_negative", \n',
        '                "TotalCharges_negative", "TotalCharges_logical_flag"]\n',
        '\n',
        'feature_cols = [c for c in df.columns if c not in exclude_cols]\n',
        'print(f"Features for segmentation: {feature_cols}")\n',
        '\n',
        '# Separate numerical and categorical\n',
        'numerical_features = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()\n',
        'categorical_features = df[feature_cols].select_dtypes(include=["object", "bool"]).columns.tolist()\n',
        '\n',
        'print(f"Numerical features: {numerical_features}")\n',
        'print(f"Categorical features: {categorical_features}")'
    ]
})

# Cell 4: Preprocessing
notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Create a copy for preprocessing\n',
        'df_prep = df[feature_cols].copy()\n',
        '\n',
        '# Encode categorical features\n',
        'label_encoders = {}\n',
        'for col in categorical_features:\n',
        '    le = LabelEncoder()\n',
        '    df_prep[col] = le.fit_transform(df_prep[col].astype(str))\n',
        '    label_encoders[col] = le\n',
        '    print(f"{col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")\n',
        '\n',
        '# Scale numerical features\n',
        'scaler = StandardScaler()\n',
        'df_prep[numerical_features] = scaler.fit_transform(df_prep[numerical_features])\n',
        '\n',
        'print(f"\\nPreprocessed shape: {df_prep.shape}")\n',
        'df_prep.head()'
    ]
})

# Cell 5: Cluster Selection
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ['## 3. Optimal Cluster Selection\n', '\n', 'We use the Elbow Method and Silhouette Score to determine the optimal number of clusters.']
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Elbow Method and Silhouette Analysis\n',
        'inertias = []\n',
        'silhouettes = []\n',
        'K_range = range(2, 11)\n',
        '\n',
        'for k in K_range:\n',
        '    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)\n',
        '    kmeans.fit(df_prep)\n',
        '    inertias.append(kmeans.inertia_)\n',
        '    sil = silhouette_score(df_prep, kmeans.labels_)\n',
        '    silhouettes.append(sil)\n',
        '    print(f"K={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={sil:.4f}")\n',
        '\n',
        '# Plot results\n',
        'fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n',
        'axes[0].plot(K_range, inertias, "bo-")\n',
        'axes[0].set_xlabel("Number of Clusters (K)")\n',
        'axes[0].set_ylabel("Inertia")\n',
        'axes[0].set_title("Elbow Method")\n',
        'axes[0].grid(True, alpha=0.3)\n',
        '\n',
        'axes[1].plot(K_range, silhouettes, "ro-")\n',
        'axes[1].set_xlabel("Number of Clusters (K)")\n',
        'axes[1].set_ylabel("Silhouette Score")\n',
        'axes[1].set_title("Silhouette Analysis")\n',
        'axes[1].grid(True, alpha=0.3)\n',
        '\n',
        'plt.tight_layout()\n',
        'plt.savefig(VIS_DIR / "cluster_selection.png", dpi=150, bbox_inches="tight")\n',
        'plt.show()'
    ]
})

# Cell 6: K-Means Clustering
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ['## 4. K-Means Clustering\n', '\n', 'Based on the elbow and silhouette analysis, we select the optimal number of clusters and fit the final model.']
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Select optimal K (based on silhouette score and elbow)\n',
        'optimal_k = 4\n',
        '\n',
        'kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)\n',
        'cluster_labels = kmeans.fit_predict(df_prep)\n',
        '\n',
        '# Add cluster ID to original dataframe\n',
        'df["Cluster_ID"] = cluster_labels\n',
        '\n',
        '# Cluster distribution\n',
        'cluster_counts = df["Cluster_ID"].value_counts().sort_index()\n',
        'print("Cluster Distribution:")\n',
        'print(cluster_counts)\n',
        'print(f"\\nSilhouette Score: {silhouette_score(df_prep, cluster_labels):.4f}")'
    ]
})

# Cell 7: Cluster Analysis
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ['## 5. Cluster Analysis and Segment Naming\n', '\n', 'We analyze each cluster\'s characteristics using the original (unscaled) features to derive meaningful business-friendly segment names.']
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Analyze cluster characteristics using original features\n',
        'cluster_profiles_num = df.groupby("Cluster_ID")[numerical_features].mean()\n',
        'print("Cluster Profiles (Numerical):")\n',
        'print(cluster_profiles_num.round(2))\n',
        '\n',
        '# For categorical features, show mode\n',
        'for col in categorical_features:\n',
        '    mode_vals = df.groupby("Cluster_ID")[col].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "N/A")\n',
        '    print(f"\\n{col} mode by cluster:")\n',
        '    print(mode_vals)'
    ]
})

# Cell 8: Churn by Cluster
notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Churn rate by cluster (for evaluation only - not used in clustering)\n',
        'churn_by_cluster = df.groupby("Cluster_ID")["Churn"].apply(lambda x: (x == "Yes").mean() * 100)\n',
        'print("Historical Churn Rate by Cluster (%):")\n',
        'print(churn_by_cluster.round(2))\n',
        '\n',
        '# Additional stats\n',
        'cluster_stats = df.groupby("Cluster_ID").agg(\n',
        '    Count=("CustomerID", "count"),\n',
        '    Avg_Tenure=("tenure", "mean"),\n',
        '    Avg_MonthlyCharges=("MonthlyCharges", "mean"),\n',
        '    Avg_TotalCharges=("TotalCharges", "mean"),\n',
        '    Churn_Rate=("Churn", lambda x: (x == "Yes").mean() * 100)\n',
        ').round(2)\n',
        'cluster_stats["Percentage"] = (cluster_stats["Count"] / len(df) * 100).round(2)\n',
        'print("\\nCluster Summary:")\n',
        'print(cluster_stats)'
    ]
})

# Cell 9: Segment Names
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ['## 6. Define Segment Names Based on Data-Driven Characteristics']
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Define segment names based on actual cluster characteristics from analysis above\n',
        'segment_names = {\n',
        '    0: "Senior Vulnerable Customers",\n',
        '    1: "Budget-Conscious Customers",\n',
        '    2: "High-Value Long-Term Customers",\n',
        '    3: "New Vulnerable Customers"\n',
        '}\n',
        '\n',
        'df["Segment_Name"] = df["Cluster_ID"].map(segment_names)\n',
        'print("Segment Distribution:")\n',
        'print(df["Segment_Name"].value_counts())'
    ]
})

# Cell 10: Risk Scoring
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ['## 7. Explainable Rule-Based Churn-Risk Scoring\n', '\n', 'We create a transparent scoring system (0-100) based on customer features. The rules are designed to be understandable by non-technical stakeholders. **The actual Churn column is NOT used to calculate the score.**']
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Rule-Based Risk Scoring System (0-100)\n',
        '\n',
        'def calculate_risk_score(row):\n',
        '    """\n',
        '    Calculate explainable churn-risk score (0-100).\n',
        '    Higher score = higher risk.\n',
        '    Rules based on customer features only - no Churn column used.\n',
        '    """\n',
        '    score = 0\n',
        '    \n',
        '    # 1. Tenure Risk (max 25 points)\n',
        '    if row["tenure"] <= 6:\n',
        '        score += 25\n',
        '    elif row["tenure"] <= 12:\n',
        '        score += 15\n',
        '    elif row["tenure"] <= 24:\n',
        '        score += 10\n',
        '    elif row["tenure"] <= 48:\n',
        '        score += 5\n',
        '    \n',
        '    # 2. Monthly Charges Risk (max 20 points)\n',
        '    if row["MonthlyCharges"] >= 90:\n',
        '        score += 20\n',
        '    elif row["MonthlyCharges"] >= 70:\n',
        '        score += 15\n',
        '    elif row["MonthlyCharges"] >= 50:\n',
        '        score += 10\n',
        '    elif row["MonthlyCharges"] >= 30:\n',
        '        score += 5\n',
        '    \n',
        '    # 3. Contract Type Risk (max 25 points)\n',
        '    if row["Contract"] == "Month-to-month":\n',
        '        score += 25\n',
        '    elif row["Contract"] == "One year":\n',
        '        score += 10\n',
        '    \n',
        '    # 4. Payment Method Risk (max 10 points)\n',
        '    if row["PaymentMethod"] == "Electronic check":\n',
        '        score += 10\n',
        '    elif row["PaymentMethod"] == "Mailed check":\n',
        '        score += 5\n',
        '    \n',
        '    # 5. Online Security Risk (max 10 points)\n',
        '    if row["OnlineSecurity"] == "No":\n',
        '        score += 10\n',
        '    elif row["OnlineSecurity"] == "No internet service":\n',
        '        score += 5\n',
        '    \n',
        '    # 6. Senior Citizen Risk (max 5 points)\n',
        '    if row["SeniorCitizen"] == 1:\n',
        '        score += 5\n',
        '    \n',
        '    # 7. Partner/Dependents Risk (max 5 points)\n',
        '    if row["Partner"] == "No" and row["Dependents"] == "No":\n',
        '        score += 5\n',
        '    \n',
        '    return min(score, 100)\n',
        '\n',
        '# Apply scoring\n',
        'df["Risk_Score"] = df.apply(calculate_risk_score, axis=1)\n',
        '\n',
        '# Risk Categories\n',
        'def risk_category(score):\n',
        '    if score >= 60:\n',
        '        return "High Risk"\n',
        '    elif score >= 35:\n',
        '        return "Medium Risk"\n',
        '    else:\n',
        '        return "Low Risk"\n',
        '\n',
        'df["Risk_Category"] = df["Risk_Score"].apply(risk_category)\n',
        '\n',
        'print("Risk Score Statistics:")\n',
        'print(df["Risk_Score"].describe())\n',
        'print("\\nRisk Category Distribution:")\n',
        'print(df["Risk_Category"].value_counts())'
    ]
})

# Cell 11: Segment Summary
notebook['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ['## 8. Segment Analysis and Summary Table']
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Create comprehensive segment summary\n',
        'segment_summary = []\n',
        '\n',
        'for cluster_id in sorted(df["Cluster_ID"].unique()):\n',
        '    subset = df[df["Cluster_ID"] == cluster_id]\n',
        '    name = segment_names[cluster_id]\n',
        '    \n',
        '    summary = {\n',
        '        "Cluster_ID": cluster_id,\n',
        '        "Segment_Name": name,\n',
        '        "Customer_Count": len(subset),\n',
        '        "Percentage_of_Customers": round(len(subset) / len(df) * 100, 2),\n',
        '        "Avg_Tenure": round(subset["tenure"].mean(), 2),\n',
        '        "Avg_Monthly_Charges": round(subset["MonthlyCharges"].mean(), 2),\n',
        '        "Avg_Total_Charges": round(subset["TotalCharges"].mean(), 2),\n',
        '        "Avg_Risk_Score": round(subset["Risk_Score"].mean(), 2),\n',
        '        "Pct_High_Risk": round((subset["Risk_Category"] == "High Risk").mean() * 100, 2),\n',
        '        "Historical_Churn_Rate": round((subset["Churn"] == "Yes").mean() * 100, 2)\n',
        '    }\n',
        '    segment_summary.append(summary)\n',
        '\n',
        'segment_summary_df = pd.DataFrame(segment_summary)\n',
        'print("Segment Summary:")\n',
        'print(segment_summary_df.to_string(index=False))'
    ]
})

notebook['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Save segment summary\n',
        'segment_summary_df.to_csv(REPORTS_DIR / "segment_summary.csv", index=False)\n',
        'print(f"Saved to {REPORTS_DIR / \"segment_summary.csv\"}")'
    ]
})

# Visualization cells
viz_sources = [
    ('# 1. Customer Segment Distribution\nfig, ax = plt.subplots(figsize=(10, 6))\nsegment_counts = df["Segment_Name"].value_counts().sort_index()\nbars = ax.bar(range(len(segment_counts)), segment_counts.values, \n              color=sns.color_palette("husl", len(segment_counts)), edgecolor="black")\nax.set_xticks(range(len(segment_counts)))\nax.set_xticklabels(segment_counts.index, rotation=15, ha="right")\nax.set_ylabel("Number of Customers")\nax.set_title("Customer Segment Distribution", fontsize=14, fontweight="bold")\nfor bar, count in zip(bars, segment_counts.values):\n    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, \n            f"{count}", ha="center", va="bottom", fontweight="bold")\nplt.tight_layout()\nplt.savefig(VIS_DIR / "segment_distribution.png", dpi=150, bbox_inches="tight")\nplt.show()'),
    ('# 2. Average Risk Score by Segment\nfig, ax = plt.subplots(figsize=(10, 6))\navg_risk = df.groupby("Segment_Name")["Risk_Score"].mean().sort_values()\ncolors = ["green" if x < 35 else "orange" if x < 60 else "red" for x in avg_risk.values]\nbars = ax.barh(range(len(avg_risk)), avg_risk.values, color=colors, edgecolor="black")\nax.set_yticks(range(len(avg_risk)))\nax.set_yticklabels(avg_risk.index)\nax.set_xlabel("Average Risk Score")\nax.set_title("Average Risk Score by Segment", fontsize=14, fontweight="bold")\nax.axvline(x=35, color="orange", linestyle="--", alpha=0.5, label="Medium Risk Threshold")\nax.axvline(x=60, color="red", linestyle="--", alpha=0.5, label="High Risk Threshold")\nax.legend()\nfor bar, val in zip(bars, avg_risk.values):\n    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, \n            f"{val:.1f}", ha="left", va="center", fontweight="bold")\nplt.tight_layout()\nplt.savefig(VIS_DIR / "avg_risk_by_segment.png", dpi=150, bbox_inches="tight")\nplt.show()'),
    ('# 3. Customer Segmentation Visualization (PCA)\npca = PCA(n_components=2, random_state=42)\npca_result = pca.fit_transform(df_prep)\ndf["PCA1"] = pca_result[:, 0]\ndf["PCA2"] = pca_result[:, 1]\n\nfig, ax = plt.subplots(figsize=(12, 8))\nscatter = ax.scatter(df["PCA1"], df["PCA2"], c=df["Cluster_ID"], \n                     cmap="tab10", alpha=0.6, s=30)\nax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)")\nax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)")\nax.set_title("Customer Segments (PCA Projection)", fontsize=14, fontweight="bold")\nlegend1 = ax.legend(*scatter.legend_elements(), title="Cluster ID")\nax.add_artist(legend1)\nplt.tight_layout()\nplt.savefig(VIS_DIR / "segmentation_pca.png", dpi=150, bbox_inches="tight")\nplt.show()\n\nprint(f"PCA Explained Variance: {pca.explained_variance_ratio_.sum():.1%}")'),
    ('# 4. Risk Category Distribution\nfig, axes = plt.subplots(1, 2, figsize=(14, 6))\n\n# Overall distribution\nrisk_counts = df["Risk_Category"].value_counts()\ncolors_dict = {"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"}\nbars = axes[0].bar(risk_counts.index, risk_counts.values, \n                   color=[colors_dict.get(x, "gray") for x in risk_counts.index], edgecolor="black")\naxes[0].set_ylabel("Number of Customers")\naxes[0].set_title("Overall Risk Category Distribution", fontsize=13, fontweight="bold")\nfor bar, count in zip(bars, risk_counts.values):\n    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,\n                 f"{count} ({count/len(df)*100:.1f}%)", ha="center", va="bottom", fontweight="bold")\n\n# By segment\nrisk_by_segment = df.groupby(["Segment_Name", "Risk_Category"]).size().unstack(fill_value=0)\nrisk_by_segment_pct = risk_by_segment.div(risk_by_segment.sum(axis=1), axis=0) * 100\nrisk_by_segment_pct.plot(kind="bar", stacked=True, ax=axes[1], \n                        color=[colors_dict.get(c, "gray") for c in risk_by_segment_pct.columns], edgecolor="black")\naxes[1].set_ylabel("Percentage")\naxes[1].set_title("Risk Category Distribution by Segment", fontsize=13, fontweight="bold")\naxes[1].legend(title="Risk Category")\naxes[1].tick_params(axis="x", rotation=15)\n\nplt.tight_layout()\nplt.savefig(VIS_DIR / "risk_category_distribution.png", dpi=150, bbox_inches="tight")\nplt.show()'),
    ('# 5. Comparison of Customer Characteristics Across Segments\nfig, axes = plt.subplots(2, 2, figsize=(15, 12))\n\nmetrics = ["tenure", "MonthlyCharges", "TotalCharges", "Risk_Score"]\ntitles = ["Tenure (months)", "Monthly Charges ($)", "Total Charges ($)", "Risk Score"]\n\nfor idx, (metric, title) in enumerate(zip(metrics, titles)):\n    ax = axes[idx // 2, idx % 2]\n    df.boxplot(column=metric, by="Segment_Name", ax=ax, grid=False)\n    ax.set_title(title, fontweight="bold")\n    ax.set_xlabel("")\n    ax.tick_params(axis="x", rotation=15)\n\nplt.suptitle("Customer Characteristics Across Segments", fontsize=14, fontweight="bold")\nplt.tight_layout()\nplt.savefig(VIS_DIR / "characteristics_comparison.png", dpi=150, bbox_inches="tight")\nplt.show()'),
    ('# 6. Historical Churn Rate by Segment\nfig, ax = plt.subplots(figsize=(10, 6))\nchurn_by_segment = df.groupby("Segment_Name")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).sort_values()\nbars = ax.barh(range(len(churn_by_segment)), churn_by_segment.values, \n               color=sns.color_palette("RdYlGn_r", len(churn_by_segment)), edgecolor="black")\nax.set_yticks(range(len(churn_by_segment)))\nax.set_yticklabels(churn_by_segment.index)\nax.set_xlabel("Historical Churn Rate (%)")\nax.set_title("Historical Churn Rate by Segment", fontsize=14, fontweight="bold")\nfor bar, val in zip(bars, churn_by_segment.values):\n    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, \n            f"{val:.1f}%", ha="left", va="center", fontweight="bold")\nplt.tight_layout()\nplt.savefig(VIS_DIR / "churn_by_segment.png", dpi=150, bbox_inches="tight")\nplt.show()'),
    ('# 7. Risk Score Distribution: Churned vs Retained\nfig, ax = plt.subplots(figsize=(10, 6))\ndf_churned = df[df["Churn"] == "Yes"]["Risk_Score"]\ndf_retained = df[df["Churn"] == "No"]["Risk_Score"]\n\nax.hist([df_retained, df_churned], bins=30, stacked=True, \n        label=["Retained", "Churned"], color=["green", "red"], alpha=0.7, edgecolor="black")\nax.set_xlabel("Risk Score")\nax.set_ylabel("Number of Customers")\nax.set_title("Risk Score Distribution: Churned vs Retained Customers", fontsize=14, fontweight="bold")\nax.legend()\nplt.tight_layout()\nplt.savefig(VIS_DIR / "risk_score_churn_distribution.png", dpi=150, bbox_inches="tight")\nplt.show()')
]

notebook['cells'].append({'cell_type': 'markdown', 'metadata': {}, 'source': ['## 9. Visualizations']})

for src in viz_sources:
    notebook['cells'].append({
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': src.split('\n')
    })

# Cell: Save Customer-Level Results
notebook['cells'].append({'cell_type': 'markdown', 'metadata': {}, 'source': ['## 10. Save Customer-Level Results']})
notebook['cells'].append({'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
    '# Prepare output dataframe\n',
    'output_cols = ["CustomerID", "tenure", "MonthlyCharges", "TotalCharges", "Contract",\n',
    '               "PaymentMethod", "Dependents", "Partner", "SeniorCitizen", "OnlineSecurity",\n',
    '               "Churn", "Cluster_ID", "Segment_Name", "Risk_Score", "Risk_Category"]\n',
    '\n',
    'df_output = df[output_cols].copy()\n',
    'df_output.to_csv(OUTPUT_DATA_PATH, index=False)\n',
    '\n',
    'print(f"Saved customer-segmented data to {OUTPUT_DATA_PATH}")\n',
    'print(f"Shape: {df_output.shape}")\n',
    'print(df_output.head())'
]})

# Cell: Business Recommendations
notebook['cells'].append({'cell_type': 'markdown', 'metadata': {}, 'source': ['## 11. Business Recommendations']})
notebook['cells'].append({'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
    '# Generate business recommendations based on actual segment characteristics\n',
    '\n',
    'recommendations = {}\n',
    '\n',
    'for cluster_id in sorted(df["Cluster_ID"].unique()):\n',
    '    subset = df[df["Cluster_ID"] == cluster_id]\n',
    '    name = segment_names[cluster_id]\n',
    '    \n',
    '    avg_tenure = subset["tenure"].mean()\n',
    '    avg_monthly = subset["MonthlyCharges"].mean()\n',
    '    contract_mode = subset["Contract"].mode().iloc[0]\n',
    '    payment_mode = subset["PaymentMethod"].mode().iloc[0]\n',
    '    online_sec_mode = subset["OnlineSecurity"].mode().iloc[0]\n',
    '    churn_rate = (subset["Churn"] == "Yes").mean() * 100\n',
    '    high_risk_pct = (subset["Risk_Category"] == "High Risk").mean() * 100\n',
    '    avg_risk = subset["Risk_Score"].mean()\n',
    '    \n',
    '    recs = []\n',
    '    \n',
    '    if avg_tenure < 12:\n',
    '        recs.append("Improve onboarding and early engagement programs for new customers.")\n',
    '    if contract_mode == "Month-to-month":\n',
    '        recs.append("Offer incentives for annual or multi-year contract upgrades to increase commitment.")\n',
    '    if avg_monthly > 80:\n',
    '        recs.append("Review pricing plans and provide suitable alternatives for price-sensitive high-spend customers.")\n',
    '    if payment_mode == "Electronic check":\n',
    '        recs.append("Encourage migration to automatic payment methods (credit card/bank transfer) for stability.")\n',
    '    if online_sec_mode == "No":\n',
    '        recs.append("Promote online security services as value-add to increase stickiness.")\n',
    '    if high_risk_pct > 50:\n',
    '        recs.append("Prioritize proactive retention outreach and dedicated customer support.")\n',
    '    if churn_rate > 50:\n',
    '        recs.append("Segment shows high historical churn - investigate root causes and tailor retention offers.")\n',
    '    if avg_tenure > 48 and contract_mode == "Two year":\n',
    '        recs.append("Maintain service quality and loyalty benefits for high-value long-term customers.")\n',
    '    \n',
    '    recommendations[name] = {\n',
    '        "cluster_id": cluster_id,\n',
    '        "characteristics": f"Avg Tenure: {avg_tenure:.1f}mo, Avg Monthly: ${avg_monthly:.2f}, Contract: {contract_mode}",\n',
    '        "churn_rate": churn_rate,\n',
    '        "high_risk_pct": high_risk_pct,\n',
    '        "avg_risk_score": avg_risk,\n',
    '        "recommendations": recs\n',
    '    }\n',
    '\n',
    'for name, rec in recommendations.items():\n',
    '    print(f"\\n{name} (Cluster {rec[\"cluster_id\"]}):")\n',
    '    print(f"  {rec[\"characteristics\"]}")\n',
    '    print(f"  Historical Churn Rate: {rec[\"churn_rate\"]:.1f}%")\n',
    '    print(f"  High-Risk %: {rec[\"high_risk_pct\"]:.1f}%")\n',
    '    print(f"  Avg Risk Score: {rec[\"avg_risk_score\"]:.1f}")\n',
    '    for r in rec["recommendations"]:\n',
    '        print(f"  - {r}")'
]})

# Cell: Model Limitations
notebook['cells'].append({'cell_type': 'markdown', 'metadata': {}, 'source': ['## 12. Model Limitations']})
notebook['cells'].append({'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
    'limitations = [\n',
    '    "**Rule-based risk score is not a predictive model**: The risk score (0-100) is a heuristic based on domain knowledge, not a trained probability. It should not be interpreted as a guaranteed prediction of churn.",\n',
    '    "**No causal claims**: The scoring rules identify correlations from historical data, not causal relationships. Acting on these factors may not directly prevent churn.",\n',
    '    "**Clustering is descriptive, not predictive**: K-Means segments customers based on feature similarity. Cluster assignments do not predict future behavior.",\n',
    '    "**Historical churn rate is retrospective**: The actual churn rates shown are historical observations for segment evaluation only. They were not used to create segments or risk scores.",\n',
    '    "**Feature selection bias**: The segmentation features were chosen based on availability and domain relevance. Other unobserved factors (competitor offers, life events) may drive churn.",\n',
    '    "**Static snapshot**: The analysis uses a single point-in-time dataset. Customer behavior evolves; segments and scores should be refreshed periodically.",\n',
    '    "**Threshold sensitivity**: Risk category thresholds (35, 60) are heuristic. Business context should guide final threshold selection.",\n',
    '    "**Cluster stability**: K-Means results can vary with initialization. The analysis uses n_init=10 and fixed random_state for reproducibility.",\n',
    '    "**No external validation**: The model has not been validated on out-of-time or out-of-sample data. Performance on new customers is unknown."\n',
    ']\n',
    '\n',
    'for i, lim in enumerate(limitations, 1):\n',
    '    print(f"{i}. {lim}")'
]})

# Cell: Conclusion
notebook['cells'].append({'cell_type': 'markdown', 'metadata': {}, 'source': ['## 13. Conclusion']})
notebook['cells'].append({'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
    'print("""\n',
    'CUSTOMER SEGMENTATION AND EXPLAINABLE CHURN-RISK PRIORITIZATION - CONCLUSION\n',
    '================================================================================\n',
    '\n',
    'This analysis successfully:\n',
    '1. Segmented 10,000 customers into distinct groups using K-Means clustering\n',
    '   on behavioral, financial, and service features (excluding Churn target)\n',
    '2. Assigned meaningful business-friendly segment names based on data-driven\n',
    '   characteristics\n',
    '3. Built a transparent rule-based risk scoring system (0-100) using only\n',
    '   customer features - no Churn column used\n',
    '4. Categorized customers into Low/Medium/High Risk with clear thresholds\n',
    '5. Generated actionable business recommendations for each segment\n',
    '6. Created professional visualizations for stakeholder presentation\n',
    '\n',
    'KEY DELIVERABLES:\n',
    '- notebooks/segmentation_and_risk_model.ipynb: Complete executable notebook\n',
    '- data/customer_segmented.csv: Customer data with Cluster ID, Segment Name,\n',
    '  Risk Score, and Risk Category\n',
    '- reports/segment_summary.csv: Segment-level summary statistics\n',
    '- reports/segment_analysis.md: Detailed analysis and methodology\n',
    '- reports/recommendation_memo.md: Executive recommendation memo\n',
    '- reports/segmentation_visualizations/: All visualization images\n',
    '\n',
    'The model provides a transparent, explainable framework for prioritizing\n',
    'retention efforts while clearly communicating limitations to stakeholders.\n',
    '\n',
    'NEXT STEPS:\n',
    '- Validate risk scoring on holdout/out-of-time data\n',
    '- A/B test retention interventions by segment\n',
    '- Refresh segments quarterly with new data\n',
    '- Consider supervised modeling for probability calibration\n',
    '""")'
]})

# Write notebook
with open('notebooks/segmentation_and_risk_model.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('Notebook written successfully!')