# app/extensions/db_helper.py
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Any
from pprint import pprint
from . import log_helper as log
from app.config.config import Config
from app.utils.db_middleware import get_current_database_name

conf = Config()

class DBHelper:
    """
    A centralized database helper for executing raw SQL queries via psycopg2.

    Manages connection lifecycle per query — each call to execute_query()
    opens a fresh connection, executes, and closes. Designed to work with
    PgBouncer in transaction pooling mode, where persistent connections
    are not viable.

    Supports multi-tenant setups by resolving the target database name
    dynamically from thread-local storage (set by middleware) on every
    connection, rather than reading it once at startup.

    Typical usage:
        db = DBHelper()

        # SELECT
        rows = db.execute_query("SELECT * FROM users WHERE active = %s", [True])

        # INSERT with RETURNING
        rows = db.execute_query(
            "INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id",
            [user_id, total]
        )

        # UPDATE
        affected = db.execute_query(
            "UPDATE products SET stock = %s WHERE id = %s",
            [new_stock, product_id]
        )

    Return value conventions:
        - List[dict]  — SELECT or any write with a RETURNING clause.
        - int         — rowcount for plain INSERT / UPDATE / DELETE / DDL.
        - None        — connection failure or unhandled exception.
    """

    # initialize
    def __init__(self):
        """
        Store base connection parameters from the application's configuration.

        The database name is intentionally excluded here and resolved
        per-connection in _get_connection(), allowing the target database
        to switch dynamically across requests (multi-tenant support).
        """
        # Store base connection parameters (without database name)
        # Database name will be determined dynamically per connection
        self.base_conn_params = {
            "user": conf.DB_USER,
            "password": conf.DB_PASSWORD,
            "host": conf.DB_HOST,
            "port": conf.DB_PORT,
        }

    def _get_connection(self):
        """
        Open and return a new psycopg2 connection for the current request's database.

        Resolves the target database name from thread-local storage via
        get_current_database_name() (populated by the tenant middleware).
        Falls back to the default database name from app config if
        no tenant is set on the current thread.

        Returns:
            connection: An open psycopg2 connection object.
            None:       If the connection attempt fails for any reason,
                        after logging the error.
        """        
        # Get database name from thread-local storage (set by middleware)
        # If not set, use default from settings
        db_name = get_current_database_name() or conf.DB_NAME

        # Build connection parameters with current database name
        conn_params = {
            **self.base_conn_params,
            "dbname": db_name,
        }

        try:
            return psycopg2.connect(**conn_params)
        except Exception as e:
            log.log_error(f"[DB ERROR] Could not connect to database: {e}")
            return None

    # execute query
    def execute_query(self, query: str, params: List[Any] = None):
        """
        Execute a raw SQL query and return the appropriate result.

        Handles SELECT, INSERT, UPDATE, DELETE, and DDL statements through
        a single unified interface. Write operations (INSERT, UPDATE, DELETE,
        CREATE, ALTER, DROP, TRUNCATE) are detected by keyword presence in
        the query string and committed automatically. A RETURNING clause on
        any write operation causes rows to be fetched and returned instead
        of the rowcount.

        Connection lifecycle:
            - A new connection is opened at the start of every call.
            - On success, the transaction is committed (writes only).
            - On exception, the transaction is rolled back.
            - The connection is always closed in the finally block.

        Args:
            query (str):            Raw SQL string with %s placeholders.
            params (List[Any]):     Query parameters matched to placeholders.
                                    Defaults to an empty list if not provided.

        Returns:
            List[dict]:  Rows as RealDictCursor dicts for SELECT queries
                         or writes with a RETURNING clause. Empty list if
                         zero rows are returned.
            int:         cur.rowcount for plain writes without RETURNING.
                         May be 0 if no rows were affected.
            None:        If the connection could not be established, or if
                         an unhandled exception occurred during execution.

        Raises:
            Nothing. All exceptions are caught, logged, and return None.

        Example:
            # SELECT
            users = db.execute_query(
                "SELECT * FROM users WHERE active = %s", [True]
            )

            # INSERT without RETURNING → returns rowcount
            count = db.execute_query(
                "INSERT INTO logs (msg) VALUES (%s)", ["started"]
            )

            # INSERT with RETURNING → returns inserted rows
            rows = db.execute_query(
                "INSERT INTO orders (user_id) VALUES (%s) RETURNING id, created_at",
                [user_id]
            )

            # UPDATE
            affected = db.execute_query(
                "UPDATE users SET active = %s WHERE id = %s", [False, user_id]
            )
        """
        log.log_query(query)
        log.log_params(str(params))

        conn = self._get_connection()
        if not conn:
            log.log_error("Unable to establish a database connection.")
            return None

        try:
            log.log_db("Connection established successfully!")

            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params or [])
                log.log_success("Query executed successfully!")

                is_write = any(
                    x in query.strip().upper()
                    for x in (
                        "INSERT",
                        "UPDATE",
                        "DELETE",
                        "CREATE",
                        "ALTER",
                        "DROP",
                        "TRUNCATE",
                    )
                )

                if is_write:
                    conn.commit()
                    log.log_success(f"Committed. Rows affected: {cur.rowcount}")
                    if cur.rowcount == 0:
                        log.log_warning("Write query matched 0 rows.")
                    # cur.description = (name, type_code, display_size,
                    #                    internal_size, precision, scale, null_ok)
                    if cur.description: # check if RETURNING clause is present
                        return cur.fetchall()
                    return cur.rowcount

                # SELECT (or write with RETURNING)
                records = cur.fetchall() if cur.description else []
                if not records:
                    log.log_warning("Query returned 0 rows.")
                else:
                    log.log_info(f"Rows fetched: {len(records)}")
                    pprint({"RECORDS": records})
                return records

        except Exception as e:
            conn.rollback() # Roll back any partial transaction on error
            log.log_error(f"Failed to execute query: {e}")
            return None

        finally:
            conn.close()
            log.log_db("Connection closed.")
