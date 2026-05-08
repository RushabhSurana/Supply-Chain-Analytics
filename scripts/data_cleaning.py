"""
============================================================
Supply Chain Analytics — Data Cleaning Script
Member 2 Responsibility | Phase 2
============================================================
Dataset  : shipment.csv
Rows     : 728 | Columns: 12
Author   : Member 2
Date     : 2024

Issues Found & Fixed
--------------------
ISSUE 1 : delivery_status — 24 missing values (NaN)
ISSUE 2 : customs_clearance_time_days — stored as string; 24 rows
          contain "On-Time" / "Delayed" instead of a number
ISSUE 3 : D_Country — 24 rows contain numeric strings (e.g. "65000")
          instead of a country name ("Singapore")
ISSUE 4 : freight_cost — 24 rows have anomalously low values (< 5)
          because the destination country data was corrupted
ROOT CAUSE: All 24 problem rows are the same 24 rows — a systematic
          data-entry corruption affecting Industrial Equipment Export
          shipments to Singapore. The columns D_Country,
          customs_clearance_time_days, and delivery_status appear to
          have been misaligned during data entry.
ISSUE 5 : date — stored as plain string; needs datetime conversion
ISSUE 6 : value/freight_cost — stored as int64/float64 (fine); verify
          no negatives or zeros
ISSUE 7 : D_Country — leading space on " India", " USA", etc.
          (stripped during cleaning)
============================================================
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# STEP 0 : Load raw data
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 0: Loading raw data")
print("=" * 60)

df = pd.read_csv("shipment.csv")

print(f"  Rows loaded     : {len(df)}")
print(f"  Columns         : {list(df.columns)}")
print()

# Snapshot of the raw issues
print("  Missing values per column (raw):")
print(df.isnull().sum().to_string())
print()
print(f"  Duplicate rows  : {df.duplicated().sum()}")
print()


# ─────────────────────────────────────────────
# STEP 1 : Identify the 24 corrupted rows
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Identifying the 24 corrupted rows")
print("=" * 60)

# These 24 rows share ALL of these symptoms simultaneously:
#   - delivery_status is NaN
#   - customs_clearance_time_days contains "On-Time" or "Delayed" (a string)
#   - D_Country contains a numeric string (e.g. "65000")
#
# Root cause: for these rows (all Industrial Equipment Exports to Singapore),
# it appears D_Country got a numeric value, delivery status text ended up in
# customs_clearance_time_days, and delivery_status itself was left blank.
#
# Recovery strategy:
#   - D_Country  → set to "Singapore" (destination column confirms this)
#   - delivery_status → rescue from customs_clearance_time_days column
#   - customs_clearance_time_days → set to NaN (true value is unknown)
#     and flag with data_quality_flag = True

corrupted_mask = df["delivery_status"].isna()
print(f"  Corrupted rows found : {corrupted_mask.sum()}")
print(f"  All are: product_category = {df.loc[corrupted_mask, 'product_category'].unique()}")
print(f"           type             = {df.loc[corrupted_mask, 'type'].unique()}")
print(f"           destination      = {df.loc[corrupted_mask, 'destination'].unique()}")
print()


# ─────────────────────────────────────────────
# STEP 2 : Add a data quality flag column
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 2: Adding data_quality_flag column")
print("=" * 60)

# Before we modify anything, flag the rows so analysts downstream
# know these values were recovered, not original.
df["data_quality_flag"] = False
df.loc[corrupted_mask, "data_quality_flag"] = True

print(f"  Rows flagged : {df['data_quality_flag'].sum()}")
print("  (These rows had D_Country, customs_clearance_time_days, and")
print("   delivery_status corrupted. Values were partially recovered.)")
print()


# ─────────────────────────────────────────────
# STEP 3 : Fix delivery_status — rescue from customs column
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 3: Fixing delivery_status (24 NaN rows)")
print("=" * 60)

# The text "On-Time" or "Delayed" that was incorrectly placed in
# customs_clearance_time_days is actually the delivery_status value.
# We recover it for the flagged rows.
df.loc[corrupted_mask, "delivery_status"] = df.loc[
    corrupted_mask, "customs_clearance_time_days"
]

print("  delivery_status after fix:")
print(df["delivery_status"].value_counts(dropna=False).to_string())
print(f"  NaN remaining : {df['delivery_status'].isna().sum()}")
print()


# ─────────────────────────────────────────────
# STEP 4 : Fix D_Country — corrupted rows → "Singapore"
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 4: Fixing D_Country for corrupted rows")
print("=" * 60)

# The destination city column shows "Singapore" for all 24 rows.
# D_Country should match → fix to "Singapore".
print("  D_Country sample BEFORE fix:")
print(df.loc[corrupted_mask, "D_Country"].head(5).to_string())

df.loc[corrupted_mask, "D_Country"] = "Singapore"

print()
print("  D_Country AFTER fix (full distribution):")
# Also strip leading/trailing whitespace from all D_Country values
df["D_Country"] = df["D_Country"].str.strip()
print(df["D_Country"].value_counts().to_string())
print()


# ─────────────────────────────────────────────
# STEP 5 : Fix customs_clearance_time_days
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 5: Fixing customs_clearance_time_days")
print("=" * 60)

# For corrupted rows: the text in this column was the delivery status.
# We've already rescued it. Now set the customs value to NaN — we
# do NOT know the true clearance time for these shipments.
df.loc[corrupted_mask, "customs_clearance_time_days"] = np.nan

# For all rows: coerce to numeric. Any remaining non-numeric entries
# (none expected after the above fix) will become NaN.
df["customs_clearance_time_days"] = pd.to_numeric(
    df["customs_clearance_time_days"], errors="coerce"
)

print(f"  dtype after conversion : {df['customs_clearance_time_days'].dtype}")
print(f"  NaN count              : {df['customs_clearance_time_days'].isna().sum()}")
print(f"  Min  : {df['customs_clearance_time_days'].min()}")
print(f"  Max  : {df['customs_clearance_time_days'].max()}")
print(f"  Mean : {df['customs_clearance_time_days'].mean():.2f}")
print()


# ─────────────────────────────────────────────
# STEP 6 : Convert date to datetime
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 6: Converting date column to datetime")
print("=" * 60)

df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")

unparsed = df["date"].isna().sum()
print(f"  dtype after conversion  : {df['date'].dtype}")
print(f"  Date range              : {df['date'].min().date()} → {df['date'].max().date()}")
print(f"  Unparseable dates       : {unparsed}")
print()


# ─────────────────────────────────────────────
# STEP 7 : Standardize text columns
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 7: Standardizing text columns")
print("=" * 60)

text_cols = ["type", "product_category", "origin", "O_Country",
             "destination", "delivery_status"]

for col in text_cols:
    before = df[col].unique()
    df[col] = df[col].str.strip().str.title()
    after = df[col].unique()
    print(f"  {col}: {sorted(after)}")

print()


# ─────────────────────────────────────────────
# STEP 8 : Validate numeric columns
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 8: Validating numeric columns (value, freight_cost)")
print("=" * 60)

for col in ["value", "freight_cost"]:
    negatives = (df[col] < 0).sum()
    zeros = (df[col] == 0).sum()
    print(f"  {col}:")
    print(f"    Negative values : {negatives}")
    print(f"    Zero values     : {zeros}")
    print(f"    Min : {df[col].min()} | Max : {df[col].max()}")
    print()

# Note the 24 corrupted rows have very low freight costs (2.2–3.3)
# These are flagged already via data_quality_flag — no further action
# needed as they are legitimate anomalies caused by the data corruption.
low_freight = df[df["freight_cost"] < 5]
print(f"  Rows with freight_cost < 5 : {len(low_freight)}")
print(f"  All are flagged rows       : {low_freight['data_quality_flag'].all()}")
print()


# ─────────────────────────────────────────────
# STEP 9 : Check for duplicates
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 9: Duplicate check")
print("=" * 60)

dupes = df.duplicated().sum()
id_dupes = df["shipment_id"].duplicated().sum()
print(f"  Full row duplicates : {dupes}")
print(f"  Duplicate IDs       : {id_dupes}")
print()


# ─────────────────────────────────────────────
# STEP 10 : Final state summary
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 10: Final cleaned dataset summary")
print("=" * 60)

print(f"  Total rows         : {len(df)}")
print(f"  Columns            : {len(df.columns)}")
print()
print("  Missing values per column (cleaned):")
print(df.isnull().sum().to_string())
print()
print("  Column dtypes:")
print(df.dtypes.to_string())
print()
print("  data_quality_flag distribution:")
print(df["data_quality_flag"].value_counts().to_string())
print()
print("  delivery_status distribution:")
print(df["delivery_status"].value_counts(dropna=False).to_string())
print()


# ─────────────────────────────────────────────
# STEP 11 : Export
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 11: Exporting cleaned dataset")
print("=" * 60)

output_path = "shipment_cleaned.csv"
df.to_csv(output_path, index=False)
print(f"  Saved to: {output_path}")
print()
print("  Cleaning complete. Hand off to Member 3 for feature engineering.")
print("=" * 60)
