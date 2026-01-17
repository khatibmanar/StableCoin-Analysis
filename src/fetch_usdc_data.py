import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone

# -----------------------------
# Configuration
# -----------------------------
ETHERSCAN_API_KEY = "API_KEY_HIDDEN"
BASE_URL = "https://api.etherscan.io/v2/api"
USDC_CONTRACT = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

PAGE = 1
OFFSET = 1000
SORT = "asc"

# -----------------------------
# Helper: get block by time
# -----------------------------
def get_block_by_time(timestamp, closest="before"):
    params = {
        "chainid": 1,
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": int(timestamp),
        "closest": closest,
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") != "1":
        raise ValueError(f"Block lookup failed: {data}")

    return int(data["result"])

# -----------------------------
# Define 30-day window
# -----------------------------
end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(days=30)

start_block = get_block_by_time(start_date.timestamp(), "before")
end_block = get_block_by_time(end_date.timestamp(), "before")

print(f"Fetching blocks {start_block} to {end_block}")

# -----------------------------
# Fetch USDC transactions
# -----------------------------
def fetch_usdc_transactions():
    all_transactions = []
    page = PAGE

    while True:
        print(f"Fetching page {page}...")

        params = {
            "chainid": 1,
            "module": "account",
            "action": "tokentx",
            "contractaddress": USDC_CONTRACT,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": OFFSET,
            "sort": SORT,
            "apikey": ETHERSCAN_API_KEY
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("status") != "1":
            print("Etherscan message:", data.get("message"))
            break

        txs = data.get("result", [])
        if not txs:
            break

        all_transactions.extend(txs)
        page += 1
        time.sleep(0.25)

    return pd.DataFrame(all_transactions)

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    df = fetch_usdc_transactions()
    print(f"Fetched {len(df)} transactions.")

    if len(df) > 0:
        df.to_csv("data/usdc_raw_30d_fail.csv", index=False)
        print("Saved data/usdc_raw_30d.csv")
    else:
        print("No transactions fetched.")
