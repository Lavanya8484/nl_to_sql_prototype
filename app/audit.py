import sqlite3, os, json, datetime
DB = os.path.join(os.path.dirname(__file__), '..', '..', 'db_files', 'db_sqlite.sqlite')
def _conn():
    return sqlite3.connect(DB)

def init():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS query_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        user_role TEXT,
        nl_query TEXT,
        generated_sql TEXT,
        result_sample TEXT
    )''')
    conn.commit()
    conn.close()

def log_query(user, nl_query, generated_sql, result_sample):
    init()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO query_history (ts,user_role,nl_query,generated_sql,result_sample) VALUES (?,?,?,?,?)",
                (datetime.datetime.utcnow().isoformat(), user, nl_query, generated_sql, json.dumps(result_sample)))
    conn.commit()
    conn.close()
