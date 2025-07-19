#!/usr/bin/env python3

"""
Run generate_descriptor_ranges.py on specific CSV file paths.

Each file will be processed using the descriptor range generator script.
Set all paths in the USER INPUT SECTION.

Usage:
    python run_generate_on_csv_list.py
"""

import subprocess
import shlex
from pathlib import Path

# ----------------------- USER INPUT SECTION -----------------------

# List of full file paths you want to process
FILE_PATHS = [
    "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/MODEL_SMILE/BOTH_Final_ML_ready_file_with_label.csv",
    # Add more paths if needed
]

# Full path to VIP (top features) CSV file
VIP_FILE = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/MODEL_SMILE/Top_70_Important_Features.csv"

# Full path to the descriptor range generation script
GENERATOR_SCRIPT = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/Automation_Script/generate_descriptor_ranges.py"

# Number of top features to keep
TOP_N = 70

# ----------------------- END USER INPUT ---------------------------

# Validate input files
for fpath in FILE_PATHS:
    if not Path(fpath).is_file():
        print(f"❌ File not found: {fpath}")
        exit(1)

if not Path(VIP_FILE).is_file():
    print(f"❌ VIP file not found: {VIP_FILE}")
    exit(1)

if not Path(GENERATOR_SCRIPT).is_file():
    print(f"❌ Generator script not found: {GENERATOR_SCRIPT}")
    exit(1)

# Run descriptor generator script on each input file
for csv_file in FILE_PATHS:
    cmd = (
        f"python \"{GENERATOR_SCRIPT}\" "
        f"--data \"{csv_file}\" "
        f"--vip \"{VIP_FILE}\" "
        f"--top_n {TOP_N}"
    )
    print(f"\n▶ Running descriptor generation on:\n  {csv_file}")
    try:
        subprocess.run(shlex.split(cmd), check=True)
        print("✅ Completed successfully.")
    except subprocess.CalledProcessError:
        print("❌ Error occurred during processing.")
        # Continue to next file if needed; or use exit(1) to stop
        # exit(1)

print("\n🎉 All descriptor generation tasks finished.")

