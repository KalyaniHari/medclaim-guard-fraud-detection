import pandas as pd
import numpy as np

# paths
cleaned_path = "../data/processed/partb_cleaned.csv"
leie_path = "../data/raw/leie.csv"
output_path = "../data/processed/partb_fraud_scored.csv"

# load cleaned part B
partb = pd.read_csv(cleaned_path)

# load LEIE excluded providers
leie = pd.read_csv(leie_path, dtype=str)
excluded_npis = set(leie['NPI'].astype(str).str.strip())

# tag excluded providers
partb['Rndrng_NPI'] = partb['Rndrng_NPI'].astype(str)
partb['Is_Excluded'] = partb['Rndrng_NPI'].isin(excluded_npis)

# Z-score anomaly detection
mean_cost = partb['Cost_per_Bene'].mean()
std_cost = partb['Cost_per_Bene'].std()

partb['Z_Score_Cost'] = (partb['Cost_per_Bene'] - mean_cost) / std_cost

# fraud risk scoring
def risk_level(z):
    if abs(z) > 3:
        return "High"
    elif abs(z) > 2:
        return "Medium"
    else:
        return "Low"

partb['Fraud_Risk_Score'] = partb['Z_Score_Cost'].apply(risk_level)

# save output
partb.to_csv(output_path, index=False)

print("Final fraud-scored file saved to:", output_path)
print("High-risk rows:", len(partb[partb['Fraud_Risk_Score'] == 'High']))
