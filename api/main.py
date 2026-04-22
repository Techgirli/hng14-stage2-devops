from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import uuid
import os

app = FastAPI()

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)
try:
    r.ping()
except redis.ConnectionError:
    raise Exception("Redis connection failed")


class JobResponse(BaseModel):
    job_id: str
    status: str


class CreateJobResponse(BaseModel):
    job_id: str


@app.get("/")
async def root():
    return {"message": "API is running"}


@app.get("/health")
async def health():
    return {"message": "healthy"}


@app.post("/jobs", response_model=CreateJobResponse)
async def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("jobs", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    r.expire(f"job:{job_id}", 3600)
    return {"job_id": job_id}


@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
