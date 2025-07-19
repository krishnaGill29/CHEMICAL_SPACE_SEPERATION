import shutil
import os

# Define source and destination paths
source_path = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/MODEL_SMILE/BOTH_Final_ML_ready_file_with_label.csv"          # Update with actual file path
destination_folder = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/DESCriptor_BASED_CHECK_TOP_70"      # Update with actual destination folder

# Create destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Build destination path
destination_path = os.path.join(destination_folder, os.path.basename(source_path))

# Move the file
shutil.move(source_path, destination_path)

print(f"File moved to: {destination_path}")

