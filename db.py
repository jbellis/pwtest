from typing import Any, Dict, List
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement


class DB:
    def __init__(self, **kwargs):
        self.cluster = Cluster(**kwargs)
        self.session = self.cluster.connect()
        self.session.default_timeout = 60

        query_cql = f"""
        SELECT body_blob
          FROM pw.embeddings_table_mock
         WHERE metadata_s['intent_type'] = 'academic'
           AND metadata_s['type'] = ?
         ORDER BY vector ANN OF ?
        LIMIT 3;
        """
        self.query_stmt = self.session.prepare(query_cql)


    def query(self, type, vector) -> List[int]:
        res = self.session.execute(self.query_stmt, (type, vector,))
        return res.all()

    def upsert_one(self, row: Dict[str, Any]) -> None:
        insert_cql = f"""
        INSERT INTO pw.embeddings_table_mock (row_id, vector, metadata_s, body_blob)
        VALUES (?, ?, ?, ?)
        """
        insert_stmt = self.session.prepare(insert_cql)
        self.session.execute(insert_stmt, (row['id'], row['vector'], row['metadata'], row['body_blob']))