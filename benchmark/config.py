import os
from pathlib import Path
from dotenv import load_dotenv

# ----------------------------------------------------
# Load .env from project root
# ----------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

# ----------------------------------------------------
# CognoDB
# ----------------------------------------------------

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USER = os.getenv("COGNODB_USER")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")

# ----------------------------------------------------
# Neo4j Aura
# ----------------------------------------------------

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# ----------------------------------------------------
# Memgraph
# ----------------------------------------------------

MEMGRAPH_URI = os.getenv("MEMGRAPH_URI")
MEMGRAPH_USER = os.getenv("MEMGRAPH_USER")
MEMGRAPH_PASSWORD = os.getenv("MEMGRAPH_PASSWORD")

# ----------------------------------------------------
# ArangoDB
# ----------------------------------------------------

ARANGODB_URL = os.getenv("ARANGODB_URL")
ARANGODB_DATABASE = os.getenv("ARANGODB_DATABASE")
ARANGODB_USER = os.getenv("ARANGODB_USER")
ARANGODB_PASSWORD = os.getenv("ARANGODB_PASSWORD")

# ----------------------------------------------------
# Apache AGE
# ----------------------------------------------------

AGE_HOST = os.getenv("AGE_HOST")
AGE_PORT = int(os.getenv("AGE_PORT", "5432"))
AGE_DATABASE = os.getenv("AGE_DATABASE")
AGE_USER = os.getenv("AGE_USER")
AGE_PASSWORD = os.getenv("AGE_PASSWORD")

def print_config():
    print("=" * 60)
    print("Benchmark Configuration")
    print("=" * 60)

    print("\nCognoDB")
    print(" URI :", COGNODB_URI)
    print(" USER:", COGNODB_USER)
    print(" PASSWORD:", "Loaded" if COGNODB_PASSWORD else "Missing")

    print("\nNeo4j")
    print(" URI :", NEO4J_URI)
    print(" USER:", NEO4J_USER)

    print("\nMemgraph")
    print(" URI :", MEMGRAPH_URI)
    print(" USER:", MEMGRAPH_USER)

    print("\nArangoDB")
    print(" URL :", ARANGODB_URL)
    print(" USER:", ARANGODB_USER)

    print("\nApache AGE")
    print(" HOST:", AGE_HOST)
    print(" DATABASE:", AGE_DATABASE)
    print(" USER:", AGE_USER)


if __name__ == "__main__":
    print_config()