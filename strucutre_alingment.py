import os
import csv
from api_example import get_align
from tqdm import tqdm

scaffold_folder = "/path/to/motif_scaffold_folder/"
motif_path = "path/to/motif_pdb/motif.pdb"

aligned_result_dict = {
    "name": [],
    "RMSD": [],
    "TM-score": [],
    "scaffold length": []
}

# Iterate through the scaffold groups
for scaffol_grps in tqdm(os.listdir(scaffold_folder), desc="Processing scaffold groups"):
    grp_pdb = os.path.join(scaffold_folder, scaffol_grps)
    for pdbs in tqdm(os.listdir(grp_pdb), desc=f"Processing pdbs in {scaffol_grps}", leave=False):
        pdb_path = os.path.join(grp_pdb, pdbs)
        # print(pdbs[:-4])
        TM_score, RMSD, Scaffold_Len = get_align(motif_path, pdb_path)
        aligned_result_dict["name"].append(pdbs[:-4])
        aligned_result_dict["RMSD"].append(RMSD)
        aligned_result_dict["TM-score"].append(TM_score)
        aligned_result_dict["scaffold length"].append(Scaffold_Len)

result_path = os.path.join(scaffold_folder, "aligned_results.csv")

# Write the results to a CSV file
with open(result_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    keys = list(aligned_result_dict.keys())
    length = len(aligned_result_dict[keys[0]])

    # Write the header
    writer.writerow(keys)
    
    # Write the data rows with tqdm progress bar
    for i in tqdm(range(length), desc="Writing rows to CSV"):
        row = [aligned_result_dict[key][i] for key in keys]
        writer.writerow(row)
