import pandas as pd
import numpy as np
import os

def generate_messy_churn_data(n=10000, seed=42):
    np.random.seed(seed)

    # 1. Base Data
    customer_ids = [f'{i:05d}' for i in range(1, n + 1)]
    tenure = np.random.randint(0, 73, size=n)
    monthly_charges = np.random.uniform(18.25, 118.75, size=n).round(2)

    # TotalCharges roughly = tenure * MonthlyCharges
    total_charges = (tenure * monthly_charges).astype(str)

    # Categorical columns
    contracts = ['Month-to-month', 'One year', 'Two year']
    payment_methods = ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']
    yes_no = ['Yes', 'No']

    data = {
        'CustomerID': customer_ids,
        'tenure': tenure,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges,
        'Contract': np.random.choice(contracts, size=n),
        'PaymentMethod': np.random.choice(payment_methods, size=n),
        'Dependents': np.random.choice(yes_no, size=n, p=[0.3, 0.7]),
        'Partner': np.random.choice(yes_no, size=n, p=[0.48, 0.52]),
        'SeniorCitizen': np.random.choice([0, 1], size=n, p=[0.84, 0.16]),
        'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], size=n),
        'Churn': np.random.choice(yes_no, size=n, p=[0.73, 0.27])
    }

    df = pd.DataFrame(data)

    # 2. Inject Messiness

    # Missing Values (~2-5% per column)
    df.loc[np.random.choice(df.index, size=200, replace=False), 'MonthlyCharges'] = np.nan
    df.loc[np.random.choice(df.index, size=300, replace=False), 'TotalCharges'] = " " # Empty strings like in real Telco data
    df.loc[np.random.choice(df.index, size=150, replace=False), 'Dependents'] = np.nan

    # Duplicates
    # Exact duplicates
    exact_dups = df.iloc[:50].copy()
    # CustomerID duplicates (same ID, different data - represents data entry error)
    id_dups = df.iloc[100:150].copy()
    id_dups['MonthlyCharges'] = id_dups['MonthlyCharges'] + 10

    df = pd.concat([df, exact_dups, id_dups], ignore_index=True)

    # Outliers (Manual injection)
    df.loc[10, 'MonthlyCharges'] = 999.0  # Extreme outlier
    df.loc[11, 'tenure'] = -5             # Logical outlier
    df.loc[12, 'MonthlyCharges'] = -50.0  # Logical outlier

    # Inconsistent Categoricals
    df.loc[df.sample(frac=0.05).index, 'Churn'] = 'yes'
    df.loc[df.sample(frac=0.03).index, 'Churn'] = 'Y'
    df.loc[df.sample(frac=0.05).index, 'Contract'] = 'month-to-month'
    df.loc[df.sample(frac=0.02).index, 'PaymentMethod'] = 'electronic check ' # trailing space

    # Logical mismatches
    # Set some TotalCharges to be way off
    df.loc[500, 'TotalCharges'] = "50000.0"

    # Final shuffle
    df = df.sample(frac=1).reset_index(drop=True)

    return df

if __name__ == "__main__":
    df = generate_messy_churn_data()
    output_path = "churn_analysis/data/originals/customer_churn_raw.csv"
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at {output_path}")
    print(f"Shape: {df.shape}")
