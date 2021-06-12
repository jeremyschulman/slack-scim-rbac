#!/usr/bin/env bash

uvicorn rbacker:api --host 0.0.0.0 --port ${SLACK_APP_PORT} --log-level debug
