# import traceback

# print(">>> run_benchmarks.py started")

# from benchmark.connectors.factory import ConnectorFactory
# from benchmark.benchmark_runner import BenchmarkRunner


# DATABASES = [
#     "cognodb",
# ]


# def print_results(result):
#     print(f"Average   : {result['Average']:.2f} ms")
#     print(f"Minimum   : {result['Minimum']:.2f} ms")
#     print(f"Maximum   : {result['Maximum']:.2f} ms")
#     print(f"P50       : {result['P50']:.2f} ms")
#     print(f"P95       : {result['P95']:.2f} ms")
#     print(f"Iterations: {result['Iterations']}")
#     print(f"Warmup    : {result['Warmup']}")


# def main():

#     print(">>> Entered main()")

#     runner = BenchmarkRunner()

#     for database in DATABASES:

#         print("\n" + "=" * 70)
#         print(f"DATABASE : {database.upper()}")
#         print("=" * 70)

#         try:

#             db = ConnectorFactory.get(database)

#             print("Creating connection...")

#             db.connect()

#             print("Verifying connection...")

#             db.verify()

#             print("Connection Successful")

#             workloads = [
#                 ("Node Count", db.node_count),
#                 ("Lookup", db.lookup),
#                 ("Traversal 1-Hop", db.traversal_1hop),
#                 ("Aggregation", db.aggregation),
#             ]

#             for workload_name, workload in workloads:

#                 print("\n" + "-" * 60)
#                 print(workload_name)
#                 print("-" * 60)

#                 try:

#                     result = runner.run(workload)

#                     print_results(result)

#                 except Exception as e:

#                     print(f"FAILED : {workload_name}")
#                     print(type(e).__name__)
#                     print(e)
#                     traceback.print_exc()

#             db.close()

#         except Exception as e:

#             print(f"FAILED TO CONNECT : {database}")
#             print(type(e).__name__)
#             print(e)
#             traceback.print_exc()

#     print("\n")
#     print("=" * 70)
#     print("BENCHMARK FINISHED")
#     print("=" * 70)


# if __name__ == "__main__":
#     main()