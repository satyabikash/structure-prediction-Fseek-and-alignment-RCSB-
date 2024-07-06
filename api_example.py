import requests
import base64
import json
import time
import tqdm

def get_align(motif_path , file_path) :
    query = {
        "context": {
            "mode": "pairwise",
            "method": {
                "name": "tm-align"
            },
            "structures": [
                {
                    "format": "pdb",
                    "selection":
                        {
                            "asym_id": "A"
                        }
                },
                {
                    "format": "pdb",
                    "selection":
                        {
                            "asym_id": "A"
                        }
                }
            ]
        }
    }

    data = {"query": json.dumps(query)}
    url = "https://alignment.rcsb.org/api/v1/structures/submit"

    scaffold_name = file_path.split('/')[-1][:-4]
    files = [
            ("files", ("motif", open(motif_path, "r"))),
            ("files", (scaffold_name, open(file_path, "r")))
        ]
    response = requests.post(url=url, params=data, files=files)

    # print(response["info"]["status"])

    job_ticket = response.text  # Replace with actual job ticket obtained after submission
    output_file = "alignment_results.json"  # Specify the output file path
    # get_alignment_results(job_ticket, output_file)
    # def get_alignment_results(job_ticket, output_file):
    url = f"https://alignment.rcsb.org/api/v1/structures/results?uuid={job_ticket}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            # print(results["info"]["status"])
            if(results["info"]["status"] == "COMPLETE"):
                for score in results['results'][0]['summary']['scores']:
                    if score['type'] == "TM-score" :
                        TM_score = score['value']
                    elif score['type'] == "RMSD" :
                        RMSD = score['value']
            else :
                time.sleep(5)
                results = response.json()
                for score in results['results'][0]['summary']['scores']:
                    if score['type'] == "TM-score" :
                        TM_score = score['value']
                    elif score['type'] == "RMSD" :
                        RMSD = score['value']
            scaffold_len = results['results'][0]['summary']['n_modeled_residues'][1]
            # time.sleep(3)
            # print("RMSD = " , RMSD ," TM-score= ",TM_score ," len = ",scaffold_len)
            return TM_score , RMSD , scaffold_len
        else:
            print(f"Failed to retrieve results. Status code: {response.status_code}")
            print(response.status_code)


    except requests.exceptions.RequestException as e:
        print(f"Error fetching results: {e}")