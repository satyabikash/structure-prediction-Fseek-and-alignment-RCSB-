from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys  # Add this import
import time
import argparse
import os 


# Set up Chrome options for headless mode (optional)
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://search.foldseek.com/search")

def fetch_struct(sequence : str) : 
    sequence_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "v-text-field__slot"))
    )
    textarea = sequence_input.find_element(By.TAG_NAME, "textarea")

    textarea.send_keys(Keys.CONTROL + "a")
    textarea.send_keys(Keys.DELETE)

    textarea.send_keys(sequence)

    predict_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'v-btn') and contains(@class, 'primary') and contains(@class, 'theme--light')]"))
    )
    predict_button.click()
    option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='v-list-item__title' and text()='Structure with ESMFold']"))
    )
    option.click()
    # Wait for the text area to be updated (you may need to use a different condition or wait time)
    updated_text = sequence

    while updated_text == sequence :
        updated_textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Enter a protein structure in PDB or mmCIF format or upload a PDB or mmCIF file.']"))
        )
        updated_text = updated_textarea.get_attribute('value')
        if updated_text != sequence : 
            break
    # Print the updated content
    return updated_text

def read_fasta(file_path):
    seq_dict = {}
    with open(file_path, "r") as file:
        key = ""
        original_key = ""
        flag = 0 
        for line in file:
            if line.startswith(">"): # identify the Key
                if key == "" :
                    key = line.split(",")[0][1:]
                    original_key = key
                    flag = 1
                else : 
                    key += "_" + line.split(",")[1][1:]
                    flag = 0
            else : # store the value 
                if flag : 
                    continue
                else : 
                    seq_dict[key] = line[:-1]
                    key = original_key # change the key
    seq_dict.popitem()
    return seq_dict

def batch_process(sequence_dict , output_directory ):
    group = next(iter(sequence_dict.items()))[0].split("_sample")[0]
    group_directory  = os.path.join(output_directory , group)
    print(group , group_directory)

    if not os.path.exists(group_directory):
        os.makedirs(group_directory) 
    # os.cwd(group_directory)
    for k in sequence_dict:
        sequence = sequence_dict[k]
        pdb_data = fetch_struct(sequence)
        with open(os.path.join(group_directory, f"{k}.pdb"), "w") as pdb_file:
            print(f"saving the pdb data to {k}")
            pdb_file.write(pdb_data)

        time.sleep(5)

# if __name__ == "main" :
argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

argparser.add_argument("--input_path", type=str, help="Path to a folder with scaffold fasta files, e.g. /home/my_pdbs/")
argparser.add_argument("--output_path", type=str, help="Path where to save pdbs predicted by ESMFOLD")

args = argparser.parse_args()

fasta_inputs = args.input_path
pdb_out_dir = args.output_path
print("is it working")
# print(fasta_inputs)
for fasta in os.listdir(fasta_inputs):
    # print(fasta)
    if fasta.endswith(".fa"):
        # print(fasta)
        batch_process(read_fasta(os.path.join(fasta_inputs,fasta)) , pdb_out_dir)
# batch_process(read_fasta(fasta_file) , )
driver.quit()




