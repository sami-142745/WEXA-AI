from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RESULTS = Path("results")
REPORTS = Path("reports")
CHARTS = Path("charts")

REPORTS.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)


# --------------------------------------------------
# Benchmark Charts
# --------------------------------------------------

def create_chart(df, workload):

    data = df[df["workload"] == workload]

    if data.empty:
        return

    plt.figure(figsize=(8, 5))

    plt.bar(
        data["database"],
        data["average"],
    )

    plt.title(workload)

    plt.ylabel("Average Latency (ms)")

    plt.xlabel("Database")

    plt.xticks(rotation=20)

    plt.tight_layout()

    filename = (
        workload.lower()
        .replace(" ", "_")
        .replace("-", "_")
        + ".png"
    )

    plt.savefig(
        CHARTS / filename,
        dpi=300,
    )

    plt.close()

    print(f"Generated {filename}")


# --------------------------------------------------
# Concurrent Charts
# --------------------------------------------------

def create_concurrent_chart(df, workload):

    data = df[df["workload"] == workload]

    if data.empty:
        return

    plt.figure(figsize=(8, 5))

    plt.bar(
        data["database"],
        data["throughput"],
    )

    plt.title(
        f"{workload} Throughput"
    )

    plt.ylabel(
        "Operations / Second"
    )

    plt.xlabel(
        "Database"
    )

    plt.xticks(rotation=20)

    plt.tight_layout()

    filename = (
        workload.lower()
        .replace(" ", "_")
        + "_throughput.png"
    )

    plt.savefig(
        CHARTS / filename,
        dpi=300,
    )

    plt.close()

    print(f"Generated {filename}")


# --------------------------------------------------
# Markdown Report
# --------------------------------------------------

def generate_report(df):

    report = "# Graph Database Benchmark Report\n\n"

    report += "## Benchmark Results\n\n"

    report += df.to_markdown(index=False)

    report += "\n\n"

    report += "## Fastest Database Per Workload\n\n"

    workloads = df["workload"].unique()

    for workload in workloads:

        subset = df[df["workload"] == workload]

        fastest = subset.sort_values(
            "average"
        ).iloc[0]

        report += (
            f"- {workload}: "
            f"**{fastest['database']}** "
            f"({fastest['average']:.2f} ms)\n"
        )

    report += "\n\n"

    report += "## Overall Ranking\n\n"

    ranking = (
        df.groupby("database")["average"]
        .mean()
        .sort_values()
    )

    for i, (db, score) in enumerate(
        ranking.items(),
        start=1,
    ):

        report += (
            f"{i}. {db} "
            f"({score:.2f} ms)\n"
        )

    Path(
        REPORTS / "report.md"
    ).write_text(
        report,
        encoding="utf-8",
    )

    print("Generated report.md")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    benchmark_csv = RESULTS / "benchmark_results.csv"

    if not benchmark_csv.exists():
        print("benchmark_results.csv not found")
        return

    benchmark_df = pd.read_csv(benchmark_csv)

    create_chart(benchmark_df, "Node Count")
    create_chart(benchmark_df, "Lookup")
    create_chart(benchmark_df, "Traversal 1-Hop")
    create_chart(benchmark_df, "Traversal 2-Hop")
    create_chart(benchmark_df, "Traversal 3-Hop")
    create_chart(benchmark_df, "Aggregation")

    generate_report(benchmark_df)

    # ----------------------------------
    # Concurrent Charts
    # ----------------------------------

    concurrent_csv = RESULTS / "concurrent_results.csv"

    if concurrent_csv.exists():

        try:

            if concurrent_csv.stat().st_size > 10:

                concurrent_df = pd.read_csv(
                    concurrent_csv
                )

                if (
                    not concurrent_df.empty
                    and "workload" in concurrent_df.columns
                ):

                    workloads = (
                        concurrent_df["workload"]
                        .unique()
                    )

                    for workload in workloads:

                        create_concurrent_chart(
                            concurrent_df,
                            workload,
                        )

                else:
                    print(
                        "Skipping concurrent charts (empty data)"
                    )

            else:
                print(
                    "Skipping concurrent charts (file empty)"
                )

        except Exception as e:

            print(
                f"Skipping concurrent charts: {e}"
            )

    print(
        "\nCharts and report generated successfully."
    )


if __name__ == "__main__":
    main()