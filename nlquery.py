import sys
from typing import List

import openai

from db import DB

# Query the database using natural language, encoding with openai first
openai.api_key = open('openai.key', 'r').read().splitlines()[0]
embed_model = "text-embedding-ada-002"

def embedding_of(text: str) -> List[float]:
    res = openai.Embedding.create(
        input=[text],
        engine=embed_model
    )
    return res['data'][0]['embedding']

print("Enter your query:")
# read the query from stdin until EOF
query = sys.stdin.read()
# encode the query using openai
print('Computing embedding...')
embedding = embedding_of(query)

print('Connecting to local C*...')
db = DB()
print('querying')
# print(db.query('ask_doubt', embedding))
print(db.query_vector_only(embedding))
