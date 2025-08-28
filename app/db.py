import sqlite3
import os
from .schema_cache import get_schema_cached

BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'db_files')
DB_MAP = {
    'postgresql': os.path.join(BASE, 'db_pg.sqlite'),
    'mysql': os.path.join(BASE, 'db_mysql.sqlite'),
    'sqlite': os.path.join(BASE, 'db_sqlite.sqlite'),
}

def get_conn(db_key):
    path = DB_MAP[db_key]
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn

engines = {'postgresql': True, 'mysql': True, 'sqlite': True}

def execute_sql_safe(db_key, sql, params):
    # Very simple param handling: sqlite3 uses ? or named :param
    conn = get_conn(db_key)
    cur = conn.cursor()
    try:
        # If params contains sqlite date expressions like date('now','-6 months') we inline them
        # For safety we only allow parameterized values for simple replacements.
        cur.execute(sql, params or {})
        rows = cur.fetchall()
        results = [dict(r) for r in rows]
        return results
    finally:
        conn.close()

def introspect_schema(db_key):
    return get_schema_cached(db_key)
