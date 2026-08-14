"""
Simple utility to export tolerance limits to an Excel file.

It looks for `tolerance_limits.csv` (created by `limits.py`) or
`statistical_tolerances.csv` (created by `statistical_analysis.py`) and
writes `pin_limits.xlsx` with two sheets: `All_Limits` and `Blob_Limits`.

Usage:
    python export_limits.py

"""

import sys
from pathlib import Path
import pandas as pd

CANDIDATES = [
    "tolerance_limits.csv",
    "statistical_tolerances.csv",
    "statistical_tolerances.csv"
]

def find_input():
    for p in CANDIDATES:
        if Path(p).exists():
            return Path(p)
    return None


def main():
    inp = find_input()
    if inp is None:
        print("Error: no input CSV found. Run `limits.py` or `statistical_analysis.py` first.")
        sys.exit(1)

    df = pd.read_csv(inp)

    # Determine which columns contain limits
    if "Lower_Limit" in df.columns and "Upper_Limit" in df.columns:
        lower_col = "Lower_Limit"
        upper_col = "Upper_Limit"
    elif "Lower_3Sigma" in df.columns and "Upper_3Sigma" in df.columns:
        lower_col = "Lower_3Sigma"
        upper_col = "Upper_3Sigma"
    elif "Lower" in df.columns and "Upper" in df.columns:
        lower_col = "Lower"
        upper_col = "Upper"
    else:
        # Try common fallback names
        candidates = [c for c in ["Lower_Limit","Lower_3Sigma","Lower"] if c in df.columns]
        candidates2 = [c for c in ["Upper_Limit","Upper_3Sigma","Upper"] if c in df.columns]
        if candidates and candidates2:
            lower_col = candidates[0]
            upper_col = candidates2[0]
        else:
            print("Error: could not find limit columns in", inp)
            print("Columns found:", ", ".join(df.columns))
            sys.exit(1)

    # Build output columns list
    out_cols = ["Feature"]
    for c in ["Mean","Std","Measured_Min","Measured_Max", lower_col, upper_col]:
        if c in df.columns and c not in out_cols:
            out_cols.append(c)

    out_df = df[out_cols]

    # Blob/pin features: start with 'B' or contain 'pin' (case-insensitive)
    mask = df["Feature"].str.startswith("B") | df["Feature"].str.lower().str.contains("pin")
    blob_df = df.loc[mask, out_cols]

    out_xlsx = Path("pin_limits.xlsx")

    with pd.ExcelWriter(out_xlsx) as writer:
        out_df.to_excel(writer, sheet_name="All_Limits", index=False)
        blob_df.to_excel(writer, sheet_name="Blob_Limits", index=False)

    print(f"Wrote: {out_xlsx} (from {inp})")


if __name__ == "__main__":
    main()
