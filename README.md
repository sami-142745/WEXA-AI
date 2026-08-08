# Graph Database Benchmark Suite

A benchmarking framework for evaluating the performance of multiple graph database systems using a real-world social network dataset.

## Overview

This project benchmarks the following graph databases:

- CognoDB
- Neo4j
- Memgraph
- ArangoDB
- Apache AGE

The benchmark evaluates:

- Data Import Performance
- Node Count Queries
- Point Lookup Queries
- Graph Traversal (1-Hop, 2-Hop, 3-Hop)
- Aggregation Queries
- Concurrent Query Throughput

---

## Dataset

Dataset Used:

**soc-pokec-relationships.txt.gz**

DATASET URL LINK 

https://uploadnow.io/f/JcvBwGp

Source:
SNAP (Stanford Network Analysis Project)

Dataset Statistics Used In Benchmark:

| Metric | Value |
|----------|----------|
| Nodes | 49,683 |
| Relationships | 100,000 |

---

## Benchmark Environment

| Parameter | Value |
|------------|---------|
| Iterations | 100 |
| Warmup Runs | 20 |
| Concurrent Workers | 10 |
| Dataset Size | 49,683 Nodes |
| Relationships | 100,000 |

---

## Project Structure

```text
benchmark/
│
├── connectors/
├── importer/
├── exporter.py
├── benchmark_runner.py
├── concurrent_runner.py
├── results.py
│
scripts/
│
├── import_dataset.py
├── run_benchmarks.py
├── run_concurrent.py
├── run_import_benchmark.py
├── generate_charts.py
│
results/
charts/
reports/
```

---

## Setup

### Clone Repository

```bash
git clone <repository-url>
cd CognoDB-Benchmark-Scaffold
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running Benchmarks

### Verify Database Connectivity

```bash
python -m scripts.run_database --db cognodb
python -m scripts.run_database --db neo4j
python -m scripts.run_database --db memgraph
python -m scripts.run_database --db arangodb
python -m scripts.run_database --db age
```

---

### Import Dataset

```bash
python -m scripts.import_dataset
```

---

### Execute Query Benchmarks

```bash
python -m scripts.run_benchmarks
```

---

### Execute Concurrent Benchmarks

```bash
python -m scripts.run_concurrent
```

---

### Generate Reports and Charts

```bash
python -m scripts.generate_charts
```

---

## Benchmark Results

### Overall Ranking

| Rank | Database | Average Latency |
|--------|----------|----------|
| 🥇 1 | Memgraph | 4.39 ms |
| 🥈 2 | Neo4j | 91.11 ms |
| 🥉 3 | Apache AGE | 263.10 ms |
| 4 | CognoDB | 331.01 ms |
| 5 | ArangoDB | 340.03 ms |

---

## Fastest Database Per Workload

| Workload | Winner | Latency |
|-----------|----------|----------|
| Node Count | Memgraph | 5.31 ms |
| Lookup | Memgraph | 5.91 ms |
| Traversal 1-Hop | Memgraph | 3.83 ms |
| Traversal 2-Hop | Memgraph | 3.58 ms |
| Traversal 3-Hop | Memgraph | 4.03 ms |
| Aggregation | Memgraph | 3.70 ms |

---

## Import Benchmark

### CognoDB

| Metric | Value |
|----------|----------|
| Nodes Imported | 49,683 |
| Relationships Imported | 100,000 |
| Total Time | 18.30 sec |
| Throughput | 5,470 relationships/sec |

---

## Concurrent Throughput

| Database | Lookup Ops/Sec | Traversal Ops/Sec |
|----------|---------------:|------------------:|
| CognoDB | 24.91 | 33.40 |
| Neo4j | 80.43 | 107.15 |
| Memgraph | 876.52 | 986.54 |
| ArangoDB | 20.19 | 29.84 |
| Apache AGE | 109.77 | 94.47 |

---

## Generated Artifacts

### Results

```text
results/
├── benchmark_results.csv
├── benchmark_results.json
├── benchmark_results.xlsx
├── concurrent_results.csv
├── concurrent_results.json
├── concurrent_results.xlsx
├── import_results.csv
├── import_results.json
├── import_results.xlsx
```

### Charts

```text
charts/
├── node_count.png
├── lookup.png
├── traversal_1_hop.png
├── traversal_2_hop.png
├── traversal_3_hop.png
├── aggregation.png
├── concurrent_lookup_throughput.png
├── concurrent_traversal_throughput.png
```

### Reports

```text
reports/
└── report.md
```

---

## Key Findings

### Memgraph

- Best overall performance.
- Lowest latency across all workloads.
- Highest concurrent throughput.
- Suitable for real-time graph analytics.

### Neo4j

- Strong and consistent performance.
- Mature ecosystem and tooling.
- Reliable traversal performance.

### Apache AGE

- Good lookup performance.
- PostgreSQL integration benefits.
- Traversal performance decreases at deeper graph depths.

### CognoDB

- Successfully completed all benchmark workloads.
- Stable import and query execution.
- Higher latency compared with Neo4j and Memgraph.

### ArangoDB

- Competitive for simple queries.
- Higher latency for deep traversals.
- Greater variance in workload performance.

---

## Conclusion

This benchmark demonstrates the performance characteristics of five graph database systems using a real-world social network dataset.

Memgraph achieved the best overall performance across all workloads, followed by Neo4j. Apache AGE provided strong PostgreSQL integration with moderate performance, while CognoDB and ArangoDB completed all workloads successfully with higher average latency.

The benchmark framework provides a reusable platform for evaluating graph databases under import, traversal, aggregation, and concurrent workloads.

## ------- ##

Mohammad Azlansami

B.Tech Artificial Intelligence & Machine Learning

Teegala Krishna Reddy Engineering College
