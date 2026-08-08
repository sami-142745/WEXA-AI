import os
import requests
from pathlib import Path

DATASET_URL = "https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz"

DATA_DIR = Path("datasets")
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "soc-pokec-relationships.txt.gz"


def download_dataset():
    if OUTPUT_FILE.exists():
        print("Dataset already exists.")
        return OUTPUT_FILE

    print("Downloading dataset...")

    response = requests.get(DATASET_URL, stream=True)
    response.raise_for_status()

    with open(OUTPUT_FILE, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("Download complete.")

    return OUTPUT_FILE


if __name__ == "__main__":
    download_dataset()