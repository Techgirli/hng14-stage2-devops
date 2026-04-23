# hng14-stage2-devops
cat > README.md << 'EOF'
# HNG Stage 2 — Microservices Job Processing System

## Prerequisites
- Docker & Docker Compose
- Git

## The Quick Start
```bash
git clone https://github.com/Techgirli/hng14-stage2-devops
cd hng14-stage2-devops
docker compose up --build
```

Visit http://localhost:3000

## The Services
| Service | Port | Description |
|---|---|---|
| Frontend | 3000 | Job submission UI |
| API | 8000 (internal) | Job creation & status |
| Worker | internal | Job processor |
| Redis | internal | Job queue |

## A Successful Startup Would Show:
All 4 containers show `healthy` status:
```bash
docker compose ps
```
EOF
