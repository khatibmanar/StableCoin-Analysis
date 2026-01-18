import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone

ETHERSCAN_API_KEY = "GGXAHHB4NNYCMMYZD7375V32S34KZ1XIG7"
BASE_URL = "https://api.etherscan.io/v2/api"
USDC_CONTRACT = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

OFFSET = 1000
CHAIN_ID = 1


def get_block_by_time(timestamp, closest="before"):
    params = {
        "chainid": CHAIN_ID,
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": int(timestamp),
        "closest": closest,
        "apikey": ETHERSCAN_API_KEY
    }
    r = requests.get(BASE_URL, params=params).json()
    if r.get("status") != "1":
        return None
    return int(r["result"])


def fetch_block_range(start_block, end_block):
    txs = []
    page = 1

    while True:
        params = {
            "chainid": CHAIN_ID,
            "module": "account",
            "action": "tokentx",
            "contractaddress": USDC_CONTRACT,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": OFFSET,
            "sort": "asc",
            "apikey": ETHERSCAN_API_KEY
        }

        r = requests.get(BASE_URL, params=params).json()

        if r.get("status") != "1":
            break

        batch = r.get("result", [])
        if not batch:
            break

        txs.extend(batch)
        page += 1
        time.sleep(0.25)

    return txs


def fetch_last_30_days():
    end_date = datetime.now(timezone.utc)
    all_txs = []

    for i in range(30):
        day_end = end_date - timedelta(days=i)
        day_start = day_end - timedelta(days=1)

        print(f"Fetching {day_start.date()}")

        start_block = get_block_by_time(day_start.timestamp(), "before")
        end_block = get_block_by_time(day_end.timestamp(), "before")

        if start_block is None or end_block is None:
            print("  Skipped (block lookup failed)")
            continue

        daily = fetch_block_range(start_block, end_block)
        print(f"  Retrieved {len(daily)} txs")

        all_txs.extend(daily)

    return pd.DataFrame(all_txs)


if __name__ == "__main__":
    df = fetch_last_30_days()
    print(f"Total fetched: {len(df)}")

    df.to_csv("data/usdc_etherscan_30d.csv", index=False)
    print("Saved data/usdc_etherscan_30d.csv")
