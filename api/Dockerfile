FROM python:3.11-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir --timeout=300 -r requirements.txt

FROM python:3.11-alpine
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# hadolint ignore=DL3018
RUN apk add --no-cache curl
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:appgroup /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]