import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans

# Test One-Hot Encoding with K-Means - detailed comparison
df = pd.read_csv('data/churn_clean.csv')

exclude_cols = ['CustomerID', 'Churn', 'tenure_outlier', 'MonthlyCharges_outlier',
                'TotalCharges_outlier', 'tenure_negative', 'MonthlyCharges_negative',
                'TotalCharges_negative', 'TotalCharges_logical_flag']
feature_cols = [c for c in df.columns if c not in exclude_cols]

numerical_features = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()
categorical_features = df[feature_cols].select_dtypes(include=['object', 'bool']).columns.tolist()

# One-Hot Encode
df_prep = df[feature_cols].copy()
ohe = OneHotEncoder(sparse_output=False, drop='first')
cat_encoded = ohe.fit_transform(df_prep[categorical_features])
cat_feature_names = ohe.get_feature_names_out(categorical_features)

df_cat = pd.DataFrame(cat_encoded, columns=cat_feature_names, index=df_prep.index)
df_prep = df_prep.drop(columns=categorical_features)
df_prep = pd.concat([df_prep, df_cat], axis=1)

scaler = StandardScaler()
df_prep[numerical_features] = scaler.fit_transform(df_prep[numerical_features])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(df_prep)

df['Cluster_OHE'] = labels

# Check churn by cluster
for cid in sorted(df['Cluster_OHE'].unique()):
    subset = df[df['Cluster_OHE'] == cid]
    churn_rate = (subset['Churn'] == 'Yes').mean() * 100
    print(f'Cluster {cid}: n={len(subset)}, Churn={churn_rate:.1f}%')
    print(f'  Tenure: {subset["tenure"].mean():.1f}, Monthly: ${subset["MonthlyCharges"].mean():.2f}')
    print(f'  Contract: {subset["Contract"].mode().iloc[0]}')
    print(f'  PaymentMethod: {subset["PaymentMethod"].mode().iloc[0]}')
    print(f'  OnlineSecurity: {subset["OnlineSecurity"].mode().iloc[0]}')
    print(f'  SeniorCitizen: {(subset["SeniorCitizen"]==1).mean()*100:.1f}%')
    print()