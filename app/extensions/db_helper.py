import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Any
from pprint import pprint


class DBHelper:

    # initialize
    def __init__(self):
        self.conn_params = {
            "dbname": "todoapp_db",
            "user": "todoapp_user",
            "password": "todoapp@786",
            "host": "localhost",
            "port": "5432",
        }

    def _get_connection(self):
        try:
            return psycopg2.connect(**self.conn_params)
        except Exception as e:
            print(f"[DB ERROR] failed to connect to db: {e}")
            return None

    # execute query
    def execute_query(self, query: str = None, params: List[Any] = None) -> List[Any]:
        print(f"QUERY: {str(query)}")
        print(f"PARAMS: {str(params)}")
        conn = self._get_connection()
        if not conn:
            print("[DB ERROR] Unable to establish a database connection.")
            return []

        try:
            print("[DB INFO] Connection established successfully!")
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query or "", params or [])
                print("[DB INFO] Query executed successfully!")
                # commit if DML
                if any((x in query.upper()) for x in ("INSERT", "UPDATE", "DELETE")):
                    conn.commit()
                    print("[DB INFO] Changes commited!")
                    print(f"[DB INFO] Records affected: {cur.rowcount}")

                records = cur.fetchall() or []
                print(f"[DB INFO] Records fetched: {len(records)}")
                pprint({"RECORDS": records or []})
                return records if records else []
        except Exception as e:
            print(f"[DB ERROR] Failed to execute query: {e}")
            return []
        finally:
            print("[DB INFO] Closing connection...")
            conn.close()
