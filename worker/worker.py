import redis
import time
import os
import signal
import sys

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=5,
    retry_on_timeout=True
)

running = True


def shutdown_handler(signum, frame):
    global running
    print("Shutting down worker gracefully...")
    running = False


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


print("Worker started...")

while running:
    try:
        job = r.brpop("job", timeout=5)

        if job:
            _, job_id = job
            process_job(job_id)

    except redis.exceptions.ConnectionError:
        print("Redis unavailable, retrying...")
        time.sleep(2)

print("Worker stopped cleanly")
sys.exit(0)
