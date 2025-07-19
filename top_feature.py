import pandas as pd

# --- Load variable importance CSVs ---
rf_path  = "/home/vishal/A_HIOT_NEW/AUTO_MATION/CHEMICAL_SPACE/Ensemble_RF_varimp.csv"
xgb_path = "/home/vishal/A_HIOT_NEW/AUTO_MATION/CHEMICAL_SPACE/Ensemble_XGB_varimp.csv"
dl_path  = "/home/vishal/A_HIOT_NEW/AUTO_MATION/CHEMICAL_SPACE/Ensemble_DL_base_varimp.csv"

rf  = pd.read_csv(rf_path)
xgb = pd.read_csv(xgb_path)
dl  = pd.read_csv(dl_path)

# --- Standardize column names for merging ---
for df, model in zip([rf, xgb, dl], ["RF", "XGB", "DL"]):
    df.rename(columns={
        "variable": "Variable",
        "scaled_importance": f"Scaled_{model}"
    }, inplace=True)

# --- Merge all three importance tables ---
merged = rf[["Variable", "Scaled_RF"]] \
    .merge(xgb[["Variable", "Scaled_XGB"]], on="Variable", how="outer") \
    .merge(dl[["Variable", "Scaled_DL"]], on="Variable", how="outer")

# --- Fill missing values (NaNs → 0) ---
merged.fillna(0, inplace=True)

# --- Compute average scaled importance ---
merged["Avg_Scaled_Importance"] = merged[["Scaled_RF", "Scaled_XGB", "Scaled_DL"]].mean(axis=1)

# --- Sort by average scaled importance ---
ranked = merged.sort_values("Avg_Scaled_Importance", ascending=False)

# --- Save output ---
ranked.to_csv("Top_Features_Ranked.csv", index=False)

# Optional: Save top N features separately
top_20 = ranked.head(25)
top_20.to_csv("/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/MODEL_SMILE/Top_70_Important_Features.csv", index=False)

print("✅ Done! Saved:")
print("- Top_Features_Ranked.csv")
print("- Top_70_Important_Features.csv")

