# NL-to-SQL Multi-DB Prototype (Minimal)
This is a minimal FastAPI prototype demonstrating:
- simple NL -> SQL translation (rule-based)
- schema introspection (SQLite used to simulate Postgres/MySQL/SQLite)
- safe parameterized execution with SQLAlchemy (demo uses sqlite3 for simplicity)
- lightweight audit logging and role-based masking (email masking)
- demo scripts and sample DBs

## How to run (locally)
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic
   ```
2. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Example query (curl):
   ```bash
   curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d '{"nl_query":"Show me all customers from California", "db":"postgresql"}'
   ```
Notes:
- This repository is a minimal demonstration. In production you'd use real Postgres/MySQL/Mongo,
  proper LLM-based NL->SQL translation, connection pooling, RBAC backends, etc.
