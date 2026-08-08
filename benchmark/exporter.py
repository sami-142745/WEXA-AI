import json
from pathlib import Path

import pandas as pd


class ResultExporter:

    def __init__(self, results):

        self.results = results

        self.output = Path("results")
        self.output.mkdir(exist_ok=True)

    # -------------------------------------------------
    # Benchmark Results
    # -------------------------------------------------

    def export_benchmarks(self):

        df = pd.DataFrame(
            self.results.benchmark_dict()
        )

        df.to_csv(
            self.output / "benchmark_results.csv",
            index=False,
        )

        df.to_json(
            self.output / "benchmark_results.json",
            orient="records",
            indent=4,
        )

        df.to_excel(
            self.output / "benchmark_results.xlsx",
            index=False,
        )

        return df

    # -------------------------------------------------
    # Concurrent Results
    # -------------------------------------------------

    def export_concurrent(self):

        df = pd.DataFrame(
            self.results.concurrent_dict()
        )

        df.to_csv(
            self.output / "concurrent_results.csv",
            index=False,
        )

        df.to_json(
            self.output / "concurrent_results.json",
            orient="records",
            indent=4,
        )

        df.to_excel(
            self.output / "concurrent_results.xlsx",
            index=False,
        )

        return df

    # -------------------------------------------------
    # Import Results
    # -------------------------------------------------

    def export_imports(self):

        df = pd.DataFrame(
            self.results.import_dict()
        )

        df.to_csv(
            self.output / "import_results.csv",
            index=False,
        )

        df.to_json(
            self.output / "import_results.json",
            orient="records",
            indent=4,
        )

        df.to_excel(
            self.output / "import_results.xlsx",
            index=False,
        )

        return df

    # -------------------------------------------------
    # Markdown Summary
    # -------------------------------------------------

    def export_summary(self):

        summary = "# Benchmark Summary\n\n"

        if self.results.benchmark_dict():

            df = pd.DataFrame(
                self.results.benchmark_dict()
            )

            summary += "## Benchmark Results\n\n"
            summary += df.to_markdown(index=False)

            summary += "\n\n"

        if self.results.concurrent_dict():

            df = pd.DataFrame(
                self.results.concurrent_dict()
            )

            summary += "## Concurrent Results\n\n"
            summary += df.to_markdown(index=False)

            summary += "\n\n"

        if self.results.import_dict():

            df = pd.DataFrame(
                self.results.import_dict()
            )

            summary += "## Import Results\n\n"
            summary += df.to_markdown(index=False)

        with open(
            self.output / "summary.md",
            "w",
            encoding="utf-8",
        ) as f:

            f.write(summary)

    # -------------------------------------------------
    # Export Everything
    # -------------------------------------------------

    def export_all(self):

        self.export_benchmarks()

        self.export_concurrent()

        self.export_imports()

        self.export_summary()

        print("\nResults exported successfully.")
        print("Location :", self.output.resolve())