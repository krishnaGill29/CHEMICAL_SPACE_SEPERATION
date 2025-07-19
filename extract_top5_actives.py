#!/usr/bin/env python3
"""
extract_top5_actives.py

  • Reads a prediction table (CSV) from FILE_IN
  • Keeps rows with Prediction==1, Reason contains "predicted",
    and Prob_Active > 0.005
  • Ranks by Prob_Active (desc) and exports the top‑5 to FILE_OUT
"""

from pathlib import Path
import pandas as pd
import sys

# ──────────────────────────────────────────────────────────────
# >>> ENTER YOUR INPUT PATH HERE <<< 
FILE_IN  = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/ACTIVE_MOLECULE_FIND/activity_predictions.csv"
# Output goes next to the input file with a new name
FILE_OUT = Path(FILE_IN).with_name("Top5_Predicted_Actives.csv")
THRESHOLD = 0.000535      # probability cut‑off
TOP_N     = 37          # how many rows to keep
# ──────────────────────────────────────────────────────────────

# 1. Load CSV ---------------------------------------------------
file_path = Path(FILE_IN).expanduser()
if not file_path.is_file():
    sys.exit(f"❌ Input file not found: {file_path}")

print(f"▶ Loading {file_path}")
df = pd.read_csv(file_path, engine="python")

# 2. Normalise column names ------------------------------------
df.columns = [c.strip() for c in df.columns]
lower_map  = {c.lower(): c for c in df.columns}

rename = {}
if "prediction"  not in lower_map:
    rename[next(k for k in lower_map if "predict" in k)] = "Prediction"
if "prob_active" not in lower_map:
    rename[next(k for k in lower_map if "prob" in k)]     = "Prob_Active"
if "reason"      not in lower_map:
    rename[next(k for k in lower_map if "reason" in k)]   = "Reason"

if rename:
    df = df.rename(columns=rename)

# 3. Coerce dtypes ---------------------------------------------
df["Prediction"]  = pd.to_numeric(df["Prediction"], errors="coerce").fillna(0).astype(int)
df["Prob_Active"] = pd.to_numeric(df["Prob_Active"], errors="coerce")

# 4. Filters ----------------------------------------------------
mask_pred   = df["Prediction"] == 1
mask_prob   = df["Prob_Active"] > THRESHOLD
mask_reason = df["Reason"].str.contains("predicted", case=False, na=False)

filtered = df[mask_pred & mask_prob & mask_reason].copy()
print(f"▶ {len(filtered)} rows pass all criteria (Prob_Active > {THRESHOLD})")

# 5. Sort & take top‑N -----------------------------------------
top_n = filtered.sort_values("Prob_Active", ascending=False).head(TOP_N)

# 6. Save result -----------------------------------------------
top_n.to_csv(FILE_OUT, index=False)
print(f"✅ Top‑{len(top_n)} actives written to {FILE_OUT}")

