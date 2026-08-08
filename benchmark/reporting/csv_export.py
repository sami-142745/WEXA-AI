import csv
from pathlib import Path


class CSVExporter:

    OUTPUT = Path("results")
    OUTPUT.mkdir(exist_ok=True)

    @staticmethod
    def save(filename, metrics):

        file = CSVExporter.OUTPUT / filename

        with open(file, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow(["Metric", "Value"])

            for key, value in metrics.items():

                if key != "samples":
                    writer.writerow([key, value])

        print(f"Saved -> {file}")