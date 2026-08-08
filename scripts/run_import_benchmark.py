import time

from benchmark.loader.importer import DatasetImporter
from benchmark.import_statistics import ImportStatistics

stats = ImportStatistics()


def benchmark_import(name, importer):

    print("=" * 60)
    print(name.upper())
    print("=" * 60)

    start = time.perf_counter()

    importer()

    elapsed = time.perf_counter() - start

    stats.add(
        database=name,
        nodes=49683,
        relationships=100000,
        seconds=elapsed,
    )

    print(f"\n{name} completed in {elapsed:.2f} seconds\n")


def main():

    benchmark_import(
        "cognodb",
        DatasetImporter().import_dataset,
    )

    stats.export()


if __name__ == "__main__":
    main()