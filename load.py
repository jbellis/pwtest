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

def upsert_row(id):
    vector = [round(random.uniform(-1.0, 1.0), 9) for _ in range(16)]
    # 99% of intents are academic
    intent_type = 'academic' if random.random() < 0.99 else None
    # types are evenly split
    type = random.choice(['ask_doubt', 'ask_concept_2'])
    # random five-letter string
    body = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))

    row = {'id': str(id), 'vector': vector, 'metadata': {'intent_type': intent_type, 'type': type}, 'body_blob': body}
    db = get_db_handle()
    db.upsert_one(row)

def main():
    print("Waiting for Cassandra schema")
    get_db_handle() # let one thread create the table + index
    time.sleep(1)

    print("Inserting data")
    num_threads = 16
    n_rows = 1_000_000
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        list(tqdm(executor.map(upsert_row, range(n_rows)), total=n_rows))

if __name__ == '__main__':
    main()
