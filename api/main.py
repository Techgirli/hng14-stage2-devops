from fastapi import FastAPI
import redis
import os

app = FastAPI()


def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job(job_id: str):
    r = get_redis()
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}
