import sqlite3, os, time
CACHE = {}
BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'db_files')
DB_MAP = {
    'postgresql': os.path.join(BASE, 'db_pg.sqlite'),
    'mysql': os.path.join(BASE, 'db_mysql.sqlite'),
    'sqlite': os.path.join(BASE, 'db_sqlite.sqlite'),
}

def introspect(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT name, sql FROM sqlite_master WHERE type IN ('table','view')")
    rows = cur.fetchall()
    schema = {}
    for name, sql in rows:
        # get columns
        try:
            cur2 = conn.cursor()
            cur2.execute(f"PRAGMA table_info('{name}')")
            cols = [r[1] for r in cur2.fetchall()]
            schema[name] = cols
        except Exception:
            schema[name] = []
    conn.close()
    return schema

def get_schema_cached(db_key):
    path = DB_MAP[db_key]
    mtime = os.path.getmtime(path)
    entry = CACHE.get(db_key)
    if entry and entry['mtime']==mtime:
        return entry['schema']
    schema = introspect(path)
    CACHE[db_key] = {'mtime': mtime, 'schema': schema}
    return schema
