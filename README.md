## ANN query with low-cardinality filtering

This repo provides scripts to test ANN queries with massively low-cardinality SAI filtering.

## Primary Usage

1. Install dependencies: `pip install -r requirements.txt`
1. Start a local Cassandra instance
1. `cqlsh < create.cqlsh`
1. `python load.py`
2. `python query.py`

Default vector dimension is 16 (modify in both create.cqlsh and db.py).  This makes loading a
decent-sized dataset much much faster -- since we primarily care about the filtering, not the
ANN query itself, this is a reasonable optimization.  

If you care about measuring realistic ANN 
performance then you should probably smash in the Neighborhood Watch openai embeddings
data instead of generating random vectors.

## Half-baked other stuff

nlquery.py accepts a natural language query, embeds it with OpenAI, and
queries the database using that embedding.  Requires a file named `openai.key` in the project directory.