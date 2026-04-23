import time

# POC Logic Implementation


def fetch_data_task() -> str:
    print("[Task 1] Connecting to external data source...")
    time.sleep(0.5)
    print("[Task 1] Downloaded 500 records.")
    return "success"


def process_data_task() -> str:
    print("[Task 2] Initializing data processor...")
    time.sleep(0.5)
    print("[Task 2] Cleaned records, removed duplicates.")
    return "success"


def store_data_task() -> str:
    print("[Task 3] Connecting to database...")
    time.sleep(0.5)
    print("[Task 3] Successfully inserted records.")
    return "success"
