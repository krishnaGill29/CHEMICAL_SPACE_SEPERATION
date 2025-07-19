#!/usr/bin/env python3

"""
Generate min / max ranges for a list of top descriptors from a variable importance file.

Usage:
    python generate_descriptor_ranges.py \
        --data BOTH_Final_ML_ready_file.csv \
        --vip Top_70_Important_Features.csv \
        --top_n 70
"""

import argparse
import pandas as pd
import pathlib
import sys

# --------------------------------------
# Argument parsing
# --------------------------------------
parser = argparse.ArgumentParser(description="Generate descriptor min/max ranges.")
parser.add_argument("--data", required=True, help="CSV file with full descriptor data")
parser.add_argument("--vip", required=True, help="CSV file with top descriptor names")
parser.add_argument("--top_n", type=int, default=70, help="Number of top descriptors to include")
args = parser.parse_args()

# --------------------------------------
# Load the dataset
# --------------------------------------
data_path = pathlib.Path(args.data)
vip_path = pathlib.Path(args.vip)

if not data_path.exists():
    sys.exit(f"❌ Data file not found: {data_path}")
if not vip_path.exists():
    sys.exit(f"❌ VIP file not found: {vip_path}")

data_df = pd.read_csv(data_path)
vip_df = pd.read_csv(vip_path)

# --------------------------------------
# Get descriptor names
# --------------------------------------
# Assume first column contains descriptor names
descriptor_column = vip_df.columns[0]
top_descriptors = vip_df[descriptor_column].head(args.top_n).tolist()

# Filter for descriptors that exist in data
existing_descriptors = [desc for desc in top_descriptors if desc in data_df.columns]

missing = set(top_descriptors) - set(existing_descriptors)
if missing:
    print(f"⚠️ The following descriptors are missing in the data and will be skipped:\n{', '.join(missing)}")

if not existing_descriptors:
    sys.exit("❌ None of the requested descriptors found in the dataset.")

# --------------------------------------
# Compute min/max for each descriptor
# --------------------------------------
ranges_df = data_df[existing_descriptors].agg(['min', 'max']).T.reset_index()
ranges_df.columns = ['Descriptor', 'min', 'max']

# Save result
output_file = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/DESCriptor_BASED_CHECK_TOP_70/training_descriptor_ranges.csv"
ranges_df.to_csv(output_file, index=False)
print(f"✅ Saved descriptor ranges to: {output_file}")

