from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory store for tests
jobs = {}


class JobRequest(BaseModel):
    task: str


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"message": "healthy"}


@app.post("/jobs")
def create_job(job: JobRequest):
    job_id = len(jobs) + 1
    jobs[job_id] = {
        "id": job_id,
        "task": job.task,
        "status": "pending"
    }
    return jobs[job_id]


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
