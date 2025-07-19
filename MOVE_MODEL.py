#!/usr/bin/env python3
"""
move_stacked_ensemble.py
────────────────────────
Move the first file whose name begins with
    StackedEnsemble_model*
from SOURCE_DIR to DEST_DIR and rename it to
    StackedEnsemble_model.<ext>

Edit SOURCE_DIR and DEST_DIR below, then run:
    python move_stacked_ensemble.py
"""

import shutil
from pathlib import Path

# ──── CONFIGURATION ────
SOURCE_DIR = Path("/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/MODEL_SMILE")   # folder to search
DEST_DIR   = Path("/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/ACTIVE_MOLECULE_FIND")   # where to move & rename
# ───────────────────────

PATTERN = "StackedEnsemble_model*"

# --- Checks -----------------------------------------------------------
if not SOURCE_DIR.is_dir():
    raise SystemExit(f"❌ Source folder not found: {SOURCE_DIR}")

DEST_DIR.mkdir(parents=True, exist_ok=True)

# --- Find the first matching file ------------------------------------
matches = sorted(SOURCE_DIR.glob(PATTERN))
if not matches:
    raise SystemExit(f"❌ No file matching '{PATTERN}' in {SOURCE_DIR}")

file_to_move = matches[0]                 # alphabetically first match
ext          = file_to_move.suffix        # preserve extension
dest_path    = DEST_DIR / f"StackedEnsemble_model{ext}"

# --- Move & rename ----------------------------------------------------
shutil.copy(str(file_to_move), dest_path)
print(f"✅ Moved {file_to_move.name}  →  {dest_path}")

