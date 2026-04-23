from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import os

app = FastAPI()

# Redis connection (test-safe)


def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

# ---------------- ROOT ----------------


@app.get("/")
def root():
    return {"message": "API is running"}

# ---------------- HEALTH ----------------


@app.get("/health")
def health():
    return {"message": "healthy"}

# ---------------- MODEL ----------------


class JobRequest(BaseModel):
    task: str

# ---------------- CREATE JOB ----------------


@app.post("/jobs")
def create_job(job: JobRequest):
    r = get_redis()

    job_id = r.incr("job:counter")

    r.hset(
        f"job:{job_id}",
        mapping={
            "id": str(job_id),
            "status": "pending",
            "task": job.task
        }
    )

    return {"id": job_id}

# ---------------- GET JOB ----------------


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    r = get_redis()

    job = r.hgetall(f"job:{job_id}")

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
