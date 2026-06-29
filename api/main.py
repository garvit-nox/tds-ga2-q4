import os, redis as r
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
client = r.from_url(redis_url, decode_responses=True)

@app.post("/hit/{key}")
async def hit(key: str):
    count = client.incr(key)
    return {"key": key, "count": count}

@app.get("/count/{key}")
async def count(key: str):
    val = client.get(key)
    return {"key": key, "count": int(val) if val else 0}

@app.get("/healthz")
async def healthz():
    try:
        client.ping()
        redis_status = "up"
    except Exception:
        redis_status = "down"
    return {"status": "ok", "redis": redis_status}
