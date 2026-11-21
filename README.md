# Customer Churn Analysis

## Objective
Reproducible exploratory analysis and data quality audit of a customer churn dataset.

## Folder Structure
- `data/`: Contains raw (`originals/`) and cleaned datasets.
- `notebooks/`: Exploratory analysis and cleaning code.
- `scripts/`: Production-ready cleaning pipeline and data generation scripts.
- `reports/`: Data quality summary and decision logs.

## Getting Started
1. **Generate Data:** Run `python scripts/generate_data.py` (if raw data is missing).
2. **Clean Data:** Run `python scripts/clean_pipeline.py`.
3. **Analyze:** Open `notebooks/analysis.ipynb` for EDA.

## Deliverables
- Cleaned CSV: `data/churn_clean.csv`
- DQ Summary: `reports/data_quality_summary.md`
