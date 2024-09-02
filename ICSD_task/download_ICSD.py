from huggingface_hub import hf_hub_download
import os
import zipfile
import sys
import argparse
from tqdm import tqdm

def prepare_download(argv=None):
    parser = argparse.ArgumentParser("Download data from QingyuLiu1/ICSD")
    parser.add_argument(
        "--file_name", 
        default="Dataset.zip",
        help="The name of the file to be downloaded"
    )
    parser.add_argument(
        "--local_dir",
        default="./../data",
        help = "The local directory to which the file is downloaded"
    )
    parser.add_argument(
        "--token",
        required=True,
        help="The access token used to access Hugging Face Hub"
    )
    args = parser.parse_args(argv)
    return args

def download(file_name, local_dir, token):
    print(f"Downloading data from Huggingface.")

    hf_hub_download(repo_id="QingyuLiu1/ICSD", filename=file_name, repo_type="dataset", local_dir=local_dir, token = token)

    print(f"{file_name} has been successfully downloaded.")

    zip_file = os.path.join(local_dir, file_name)
    
    # with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    #     zip_ref.extractall(local_dir) 

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        files = zip_ref.namelist()
        for file in tqdm(files, desc=f"Extracting {file_name}", unit="file"):
            zip_ref.extract(member=file, path=local_dir)
        
    print(f"The unzipping of {file_name} has completed.")

if __name__ == '__main__':
    args = prepare_download()
    download(args.file_name, args.local_dir, args.token)