import json
from pathlib import Path


class JSONExporter:

    OUTPUT = Path("results")
    OUTPUT.mkdir(exist_ok=True)

    @staticmethod
    def save(filename, metrics):

        file = JSONExporter.OUTPUT / filename

        clean = {}

        for k, v in metrics.items():

            if k != "Samples":
                clean[k] = v

        with open(file, "w") as f:
            json.dump(clean, f, indent=4)

        print(f"JSON Saved -> {file}")