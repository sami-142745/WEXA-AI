import time
from pathlib import Path

import pandas as pd


class ImportStatistics:

    def __init__(self):

        self.rows = []

    def add(
        self,
        database,
        nodes,
        relationships,
        seconds,
    ):

        self.rows.append(
            {
                "Database": database,
                "Nodes": nodes,
                "Relationships": relationships,
                "Import Time (sec)": round(seconds, 2),
                "Nodes/sec": round(nodes / seconds, 2),
                "Relationships/sec": round(
                    relationships / seconds,
                    2,
                ),
            }
        )

    def export(self):

        Path("results").mkdir(exist_ok=True)

        df = pd.DataFrame(self.rows)

        df.to_csv(
            "results/import_results.csv",
            index=False,
        )

        df.to_json(
            "results/import_results.json",
            orient="records",
            indent=4,
        )

        df.to_excel(
            "results/import_results.xlsx",
            index=False,
        )

        print("\nImport benchmark exported.")