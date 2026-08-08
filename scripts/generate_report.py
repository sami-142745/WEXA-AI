from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RESULTS = Path("results")
REPORTS = Path("reports")
CHARTS = Path("charts")

REPORTS.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)


def create_chart(df, workload):

    data = df[df["workload"] == workload]

    if data.empty:
        return

    plt.figure(figsize=(8,5))

    plt.bar(
        data["database"],
        data["average"],
    )

    plt.title(workload)

    plt.ylabel("Average Latency (ms)")

    plt.xticks(rotation=20)

    plt.tight_layout()

    filename = workload.lower().replace(" ", "_") + ".png"

    plt.savefig(
        CHARTS / filename,
        dpi=300,
    )

    plt.close()

    print(f"Generated {filename}")


def generate_report(df):

    report = "# Benchmark Report\n\n"

    report += "## Benchmark Results\n\n"

    report += df.to_markdown(index=False)

    report += "\n\n"

    report += "## Summary\n\n"

    fastest = (
        df.groupby("database")["average"]
        .mean()
        .sort_values()
    )

    report += (
        f"Fastest Database: **{fastest.index[0]}**\n\n"
    )

    Path(
        REPORTS / "report.md"
    ).write_text(report, encoding="utf-8")

    print("Generated report.md")


def main():

    csv = RESULTS / "benchmark_results.csv"

    if not csv.exists():

        print("Run benchmarks first.")

        return

    df = pd.read_csv(csv)

    create_chart(df, "Node Count")
    create_chart(df, "Lookup")
    create_chart(df, "Traversal 1-Hop")
    create_chart(df, "Traversal 2-Hop")
    create_chart(df, "Traversal 3-Hop")
    create_chart(df, "Aggregation")

    generate_report(df)

    print("\nReport generated successfully.")


if __name__ == "__main__":
    main()