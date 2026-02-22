from fastapi import FastAPI
from app.db.database import engine

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ai content detector is working"}

@app.get("/test_db")
def test_db():
    try:
        with engine.connect() as connection:
            return { "status" : "connected successfully"}
    except Exception as e:
        return {"error", str(e)}