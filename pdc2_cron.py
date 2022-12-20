#!/usr/bin/python

import zipfile, requests, os
from io import BytesIO


dump_folder = "pecosdump"

if not os.path.exists(dump_folder):
    os.mkdir(dump_folder)

def get_dataset_uuid():
    res = requests.get('https://data.cms.gov/data-api/v1/dataset-type')
    for x in res.json()["data"]:
        if x["name"] == "Medicare Fee-For-Service  Public Provider Enrollment":
            return x["latest_version_uuid"]

def download(uuid):
    res = requests.get(f'https://data.cms.gov/data-api/v1/dataset/{uuid}/resources')
    titles = ["Reassignment Sub-File", "Address Sub-File", "Secondary Specialty Sub-File"]
    for c, file in enumerate([x for x in res.json()["data"] if x["title"] in titles]):
        downloaded = 0
        file_name = file["file_name"]
        file_url = file["file_url"]
        with open(f"{dump_folder}/{file_name}", "wb") as f:
            with requests.get(file_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=1024):
                    downloaded += len(chunk)
                    print(f"({c+1}/4) Downloding {file_name} {downloaded / 1024 / 1024:.2f} MB", end="\r", flush=True)
                    f.write(chunk)
        print()

    res = requests.head(f'https://data.cms.gov/data-api/v1/dataset/{uuid}/data-viewer?_format=csv')
    file_name = res.headers['Content-Disposition'].split('filename=')[1]
    downloaded = 0
    content = BytesIO()
    with requests.get(f'https://data.cms.gov/data-api/v1/dataset/{uuid}/data-viewer?_format=csv', stream=True) as r:
        for chunk in r.iter_content(chunk_size=1024):
            downloaded += len(chunk)
            print(f"(4/4) Downloding {file_name.replace('.zip', '.csv')} {downloaded / 1024 / 1024:.2f} MB", end="\r", flush=True)
            content.write(chunk)
    content.seek(0)
    zip_file = zipfile.ZipFile(content)
    zip_file.extractall(dump_folder)

    subprocess.run(["bash", "/home/ubuntu/pdc/pdc_dump_to_s3.sh"])
    subprocess.run(["bash", "/home/ubuntu/pdc/pdc_clean.sh"])


if __name__ == "__main__":
    uuid = get_dataset_uuid()
    download(uuid)