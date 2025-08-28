from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(
    title="🌐 NL → SQL Prototype API",
    description="Convert plain English queries into SQL 🚀",
    version="1.0.0"
)

# Set template folder
templates = Jinja2Templates(directory="templates")

# Request model
class QueryRequest(BaseModel):
    query: str
    db: str

# Root
@app.get("/", tags=["Welcome"])
def read_root():
    return {"message": "Welcome to the NL → SQL Prototype API 🚀. Go to /docs to try it out."}

# Query endpoint
@app.post("/query", tags=["Query"])
def run_query(request: QueryRequest):
    return {
        "sql_query": f"SELECT * FROM table WHERE condition = '{request.query}'",
        "db": request.db
    }

# Schema endpoint
@app.get("/schema/{db_name}", tags=["Schema"])
def get_schema(db_name: str):
    return {"db": db_name, "tables": ["users", "orders", "products"]}

# 🔹 UI route (new)
@app.get("/ui", response_class=HTMLResponse, tags=["UI"])
def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
