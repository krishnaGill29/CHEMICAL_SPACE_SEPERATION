import os
from rdkit import Chem
from rdkit.Chem import AllChem

input_path = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/MODEL_SMILE/smile.txt"  # Replace with your actual filename
output_dir = "/home/vishal/A_HIOT_NEW/AUTO_MATION_CHEMICAL_SEPERATION/AUTOMATION_DATA/RANDOM_MOLECULES/SDF"
os.makedirs(output_dir, exist_ok=True)

with open(input_path, "r") as f:
    for idx, line in enumerate(f, start=1):
        smi = line.strip()
        if not smi:
            continue  # skip empty lines

        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            print(f"[ERROR] Invalid SMILES at line {idx}: {smi}")
            continue

        mol = Chem.AddHs(mol)

        # Try to embed 3D coordinates
        embed_result = AllChem.EmbedMolecule(mol, randomSeed=0xf00d)
        if embed_result != 0:
            print(f"[ERROR] 3D embedding failed for SMILES at line {idx}: {smi}")
            continue

        try:
            AllChem.UFFOptimizeMolecule(mol)
        except Exception as e:
            print(f"[ERROR] Optimization failed for molecule at line {idx}: {e}")
            continue

        # Save SDF
        fname = os.path.join(output_dir, f"molecule_{idx:03d}.sdf")
        writer = Chem.SDWriter(fname)
        writer.write(mol)
        writer.close()
        print(f"[OK] Wrote {fname}")
