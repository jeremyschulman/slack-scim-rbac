#!/usr/bin/env bash

uvicorn clicker:api \
  --host 0.0.0.0 \
  --port ${SLACK_APP_PORT} \
  --reload
