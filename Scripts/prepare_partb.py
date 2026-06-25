import pandas as pd
import numpy as np

input_path = "../data/raw/partb_2022.csv"
output_path = "../data/processed/partb_cleaned.csv"

chunksize = 200_000  # adjust if needed

keep_cols = [
    "Rndrng_NPI",
    "Rndrng_Prvdr_Last_Org_Name",
    "Rndrng_Prvdr_First_Name",
    "Rndrng_Prvdr_State_Abrvtn",
    "HCPCS_Cd",
    "HCPCS_Desc",
    "Tot_Benes",
    "Tot_Srvcs",
    "Avg_Mdcr_Pymt_Amt"
]

first_chunk = True

for chunk in pd.read_csv(input_path, chunksize=chunksize, low_memory=False):
    
    # keep only relevant columns
    chunk = chunk[keep_cols]

    # convert numeric fields
    for col in ["Tot_Benes", "Tot_Srvcs", "Avg_Mdcr_Pymt_Amt"]:
        chunk[col] = (
            chunk[col]
            .astype(str)
            .str.replace("$", "")
            .str.replace(",", "")
            .astype(float)
        )

    # feature engineering
    chunk["Total_Cost"] = chunk["Tot_Srvcs"] * chunk["Avg_Mdcr_Pymt_Amt"]
    
    chunk["Cost_per_Bene"] = chunk["Total_Cost"] / chunk["Tot_Benes"].replace({0: np.nan})

    # append processed chunk
    chunk.to_csv(output_path, mode="a", index=False, header=first_chunk)
    
    first_chunk = False

    print("Processed:", len(chunk), "rows")

print("DONE. Cleaned file saved to:", output_path)
