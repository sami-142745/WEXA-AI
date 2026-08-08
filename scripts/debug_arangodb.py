import requests
from benchmark.config import (
    ARANGODB_URL,
    ARANGODB_USER,
    ARANGODB_PASSWORD,
)

print("URL:", ARANGODB_URL)

response = requests.get(
    f"{ARANGODB_URL}/_api/version",
    auth=(ARANGODB_USER, ARANGODB_PASSWORD),
)

print("Status Code:", response.status_code)
print("Headers:", response.headers.get("content-type"))
print("Body:")
print(response.text)