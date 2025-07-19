import shutil
import os

# Define source and destination directories
source_path = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/RANDOM_MOLCULES_PUT/random_molecules_descriptors.csv"
destination_folder = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/ACTIVE_MOLECULE_FIND"

# Create destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Loop through each file in the source directory
for filename in os.listdir(source_path):
    source_file = os.path.join(source_path, filename)
    destination_file = os.path.join(destination_folder, filename)

    # Check if it's a file (not a directory)
    if os.path.isfile(source_file):
        shutil.copy(source_file, destination_file)
        print(f"Moved: {source_file} --> {destination_file}")

print("All files moved successfully.")

