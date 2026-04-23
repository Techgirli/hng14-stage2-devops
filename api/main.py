from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


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
    job_id = str(len(jobs) + 1)

    jobs[job_id] = {
        "id": job_id,
        "task": job.task,
        "status": "queued"
    }

    return {"id": job_id}


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return jobs[job_id]
