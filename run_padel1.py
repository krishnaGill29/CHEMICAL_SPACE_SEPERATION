import subprocess

# Define internal paths
padel_jar = "/home/vishal/A_HIOT_NEW/PaDEL-Descriptor/PaDEL-Descriptor.jar"
input_dir = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/RANDOM_MOLECULES/SDF"
output_file = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/RANDOM_MOLECULES/PADEL/descriptors_output1.csv"

# Construct the command
command = [
    "java", "-jar", padel_jar,
    "-2d",
    "-dir", input_dir,
    "-file", output_file
]

# Run the command
try:
    subprocess.run(command, check=True)
    print("Descriptor calculation completed successfully.")
except subprocess.CalledProcessError as e:
    print("An error occurred while running PaDEL-Descriptor:")
    print(e)

