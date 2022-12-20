#!/usr/bin/python

import zipfile, requests, os, subprocess
from io import BytesIO

#!/usr/bin/python

import zipfile, requests, os
from io import BytesIO


dump_folder = "pdcdump"

if not os.path.exists(dump_folder):
    os.mkdir(dump_folder)

def get_url():
    res = requests.get('https://data.cms.gov/provider-data/api/1/pdc/topics/current-zip')
    if "Doctors and clinicians" in res.json():
        return res.json()["Doctors and clinicians"]["2022"]["url"]
    print("Error getting url")
    exit()

def download(url):
    file_name = url.split("/")[-1]
    downloaded = 0
    content = BytesIO()
    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(chunk_size=1024):
            downloaded += len(chunk)
            print(f"Downloading {file_name} {downloaded / 1024 / 1024:.2f} MB", end="\r", flush=True)
            content.write(chunk)
    content.seek(0)
    zip_file = zipfile.ZipFile(content)
    zip_file.extractall(dump_folder)

    subprocess.run(["bash", "/home/ubuntu/pdc/pdc_dump_to_s3.sh"])

if __name__ == "__main__":
    url = get_url()
    download(url)