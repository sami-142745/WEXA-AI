from pathlib import Path


class MarkdownReport:

    @staticmethod
    def write(results):

        report = Path("README_RESULTS.md")

        with open(report, "w", encoding="utf-8") as f:

            f.write("# Benchmark Results\n\n")

            for name, metrics in results.items():

                f.write(f"## {name}\n\n")

                f.write("| Metric | Value |\n")
                f.write("|--------|------:|\n")

                for k, v in metrics.items():

                    if k != "Samples":
                        f.write(f"| {k} | {v} |\n")

                f.write("\n")

        print("README_RESULTS.md generated.")