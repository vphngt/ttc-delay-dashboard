import requests
import pandas as pd
from pathlib import Path

# ----- Configuration -----
BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

DATASETS = {
    "bus": "ttc-bus-delay-data",
    "streetcar": "ttc-streetcar-delay-data",
    "subway": "ttc-subway-delay-data"
}

RAW_DIR = Path("../data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


# ----- Functions -----
def get_package(package_id):
    url = BASE_URL + "/api/3/action/package_show"
    response = requests.get(url, params={"id": package_id})
    response.raise_for_status()

    return response.json()["result"]


def is_delay_dataset(resource):
    return (
        "2025" in resource["name"].lower()
        and resource["format"].lower() == "csv"
    )


def is_lookup_dataset(resource):
    return (
        "code" in resource["name"].lower()
        and resource["format"].lower() == "csv"
    )

def download_dataset(mode, package_id):
    print(f"\n========== {mode.upper()} ==========")
    package = get_package(package_id)

    for resource in package["resources"]:
        # only download necessary csv
        if not is_delay_dataset(resource) and not is_lookup_dataset(resource):
            continue

        print(f"Resource: {resource['name']}")
        print(f"Format: {resource['format']}")
        print(f"Datastore Active: {resource['datastore_active']}")

        extension = resource["format"].lower()

        if is_lookup_dataset(resource):
            file_name = f"{package_id}-lookup.{extension}"
        else:
            file_name = f"{package_id}-2025.{extension}"

        file_path = RAW_DIR / file_name

        # if they stores it in the datastore
        if resource["datastore_active"]:
            url = BASE_URL + "/datastore/dump/" + resource["id"]
            print("Downloading CSV...")

            csv_data = requests.get(url)
            csv_data.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(csv_data.content)

            print(f"Saved to {file_path}")

        # otherwise download directly from file URL
        else:
            file_url = resource["url"]
            print("Downloading file...")

            file_data = requests.get(file_url)
            file_data.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(file_data.content)

            print(f"Saved to {file_path}")


# ----- Main -----
if __name__ == "__main__":
    for mode, package_id in DATASETS.items():
        download_dataset(mode, package_id)

    print("\nAll datasets downloaded successfully!")