# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from os import environ
import sys
import logging

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from .app_data import api, app
from . import app_listeners  # noqa

# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------

ENV_VARS = ["SLACK_APP_TOKEN", "SLACK_BOT_TOKEN", "SLACK_SCIM_TOKEN"]

slack_websocket = AsyncSocketModeHandler(app)


@api.on_event("startup")
async def demo_startup():
    logging.basicConfig(level=logging.INFO)

    if missing := [envar for envar in ENV_VARS if not environ.get(envar)]:
        sys.exit(f"Missing required environment variables: {missing}")

    # start the websocket handler to consume messages from Slack
    await slack_websocket.start_async()
