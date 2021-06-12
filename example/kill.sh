#!/usr/bin/env bash

if [[ -z "$SLACK_APP_PORT" ]]; then
  echo "Missing $SLACK_APP_PORT" && exit
fi

lsof -t -i "tcp:${SLACK_APP_PORT}" | xargs kill -9

