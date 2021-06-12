# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

import sys
from os import environ
import logging
from importlib import import_module

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from .app_data import api, app

# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------

ENV_VARS = ["SLACK_APP_TOKEN", "SLACK_BOT_TOKEN", "SLACK_SCIM_TOKEN"]

slack_websocket = AsyncSocketModeHandler(app)


@api.on_event("startup")
async def demo_startup():
    print("Starting Rbacker ...")
    logging.basicConfig(level=logging.INFO)

    import_module("rbacker.app_handlers")
    import_module("rbacker.app_errors")

    if missing := [envar for envar in ENV_VARS if not environ.get(envar)]:
        sys.exit(f"Missing required environment variables: {missing}")

    # start the websocket handler to consume messages from Slack

    await slack_websocket.start_async()
