#!/bin/bash
set -e

echo "Starting integration test..."

RESPONSE=$(curl -s -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -d '{"task":"test"}')

echo "Response: $RESPONSE"

JOB_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Job ID: $JOB_ID"

for i in $(seq 1 30); do
  STATUS=$(curl -s http://localhost:3000/jobs/$JOB_ID \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: $STATUS"
  if [ "$STATUS" = "completed" ]; then
    echo "Integration test passed!"
    exit 0
  fi
  sleep 2
done

echo "Integration test failed - job did not complete"
exit 1
