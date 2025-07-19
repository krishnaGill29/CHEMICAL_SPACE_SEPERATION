import pandas as pd
import h2o
import numpy as np

# -------------------- CONFIGURATION -----------------------
INPUT_CSV = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/RANDOM_MOLECULES/PADEL/descriptors_output1.csv"
RANGE_CSV = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/DESCriptor_BASED_CHECK_TOP_70/training_descriptor_ranges.csv"
MODEL_PATH = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/ACTIVE_MOLECULE_FIND/StackedEnsemble_model"
OUTPUT_CSV = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/ACTIVE_MOLECULE_FIND/activity_predictions.csv"

BUFFER_RATIO = 0.10  # 10% flexibility beyond training descriptor range

# -------------------- LOAD DATA ---------------------------
print("▶ Loading descriptors …")
df = pd.read_csv(INPUT_CSV)
ranges = pd.read_csv(RANGE_CSV).set_index("Descriptor").sort_index()
TOP20 = list(ranges.index)
meta_cols = [c for c in df.columns if c.lower() in ["name", "smiles", "id"]]

# Sanity check
missing_cols = [c for c in TOP20 if c not in df.columns]
if missing_cols:
    raise ValueError(f"❌ Input CSV is missing required descriptors: {missing_cols}")
desc_df = df[TOP20]

# -------------------- START H2O ---------------------------
print("▶ Initializing H2O and loading model …")
h2o.init(max_mem_size="4G")
model = h2o.load_model(str(MODEL_PATH))

# -------------------- PREDICT -----------------------------
results = []
for idx, row in desc_df.iterrows():
    record = df.loc[idx, meta_cols].to_dict()
    desc_vals = row.to_dict()

    # Check for NaN
    if row.isnull().any():
        record.update({
            "Prediction": "Decoy",
            "Prob_Active": "",
            "Reason": "Missing descriptor(s)"
        })
        results.append(record)
        continue

    # Applicability Domain check with buffer
    out_of_range = False
    fail_reason = ""
    for d in TOP20:
        min_val, max_val = ranges.loc[d, "min"], ranges.loc[d, "max"]
        buffer = (max_val - min_val) * BUFFER_RATIO
        min_allowed, max_allowed = min_val - buffer, max_val + buffer
        val = desc_vals[d]
        if val < min_allowed or val > max_allowed:
            out_of_range = True
            fail_reason = f"{d}: {val:.3f} not in [{min_allowed:.3f}, {max_allowed:.3f}]"
            break

    if out_of_range:
        record.update({
            "Prediction": "Decoy",
            "Prob_Active": "",
            "Reason": f"Out-of-domain ({fail_reason})"
        })
        results.append(record)
        continue

    # In-domain prediction
    h2o_row = h2o.H2OFrame(pd.DataFrame([desc_vals]))
    pred_df = model.predict(h2o_row).as_data_frame().iloc[0]
    record.update({
        "Prediction": pred_df["predict"],         # 0 or 1
        "Prob_Active": pred_df["p1"],             # probability for class 1 (Active)
        "Reason": "Predicted"
    })
    results.append(record)

# -------------------- SAVE & EXIT -------------------------
out = pd.DataFrame(results)
out.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Saved predictions → {OUTPUT_CSV}")

h2o.cluster().shutdown()

