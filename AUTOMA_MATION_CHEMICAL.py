import os
import subprocess

# STEP 1: Create main folder
main_folder = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA"
os.makedirs(main_folder, exist_ok=True)
print(f"[STEP 1] Created main folder: {main_folder}")

# STEP 2: Create subfolders inside AUTOMATION_DATA
subfolders = [
    "ACTIVE_MOLECULE_FIND",
    "DESCriptor_BASED_CHECK_TOP_70",
    "RANDOM_MOLECULES/PADEL",
    "RANDOM_MOLECULES/SDF"
]

for subfolder in subfolders:
    path = os.path.join(main_folder, subfolder)
    os.makedirs(path, exist_ok=True)
    print(f"[STEP 2] Created subfolder: {path}")

# Define script paths
scripts = [
    "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/Automation_Script/top_feature.py",            # STEP 3
    "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/Automation_Script/sdf.py",                    # STEP 4
    "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/Automation_Script/run_padel1.py",            # STEP 5
    "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/Automation_Script/find.py",                  # STEP 6
    "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/Automation_Script/MOVE_MODEL.py",            # STEP 7
    "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/Automation_Script/ACTIVE_PREDICTIONs.py",    # STEP 8
    "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/Automation_Script/extract_top5_actives.py"   # STEP 9
]

# Execute each Python script step-by-step
for idx, script in enumerate(scripts, start=3):
    try:
        subprocess.run(["python3", script], check=True)
        print(f"[STEP {idx}] Successfully ran: {script}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to run {script}")
        print(e)
        break  # Stop on failure

