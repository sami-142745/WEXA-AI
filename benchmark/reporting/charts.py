import matplotlib.pyplot as plt
from pathlib import Path


class ChartGenerator:

    OUTPUT = Path("charts")
    OUTPUT.mkdir(exist_ok=True)

    @staticmethod
    def bar_chart(title, metrics, filename):

        names = list(metrics.keys())
        values = list(metrics.values())

        plt.figure(figsize=(8,5))
        plt.bar(names, values)

        plt.title(title)
        plt.ylabel("Milliseconds")

        plt.tight_layout()

        file = ChartGenerator.OUTPUT / filename

        plt.savefig(file)

        plt.close()

        print(f"Chart Saved -> {file}")