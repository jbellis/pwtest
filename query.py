import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from tqdm.auto import tqdm

from db import DB

thread_local_storage = threading.local()

def get_db_handle():
    if not hasattr(thread_local_storage, 'db_handle'):
        thread_local_storage.db_handle = DB()
    return thread_local_storage.db_handle

def query_one(_):
    vector = [round(random.uniform(-1.0, 1.0), 9) for _ in range(16)]
    type = random.choice(['ask_doubt', 'ask_concept_2'])
    db = get_db_handle()
    db.query(type, vector)

def main():
    print("Waiting for Cassandra schema")
    get_db_handle() # let one thread create the table + index
    time.sleep(1)

    print("Querying data")
    num_threads = 8
    n_rows = 1_000
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        list(tqdm(executor.map(query_one, range(n_rows)), total=n_rows))

if __name__ == '__main__':
    main()
