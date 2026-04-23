FROM python:3.11-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

COPY . .
RUN chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import redis; r = redis.Redis(host='redis'); r.ping()" || exit 1

CMD ["python", "worker.py"] 
