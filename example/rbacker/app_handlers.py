import re
import json

from slack_bolt.async_app import (
    AsyncBoltContext as BoltContext,
    AsyncBoltRequest as BoltRequest,
)
from slack_bolt.async_app import AsyncSay as Say

from slack_rbac.middleware import AsyncSlackScimRBAC

from .app_data import app


@app.event("app_mention")
async def app_mention(context: BoltContext, say: Say, event: dict):
    await say(f"You mentioned me <@{context.user_id}>?")


# -----------------------------------------------------------------------
# Messages to the app in the app specific channel
# -----------------------------------------------------------------------


@app.message(re.compile("hi", re.I))
async def app_say_ohai(context: BoltContext, say: Say):
    await say(f"Ohai <@{context.user_id}>")


@app.message(re.compile("show port", re.I))
async def app_show_port(context: BoltContext, say: Say):
    await say(f"getting port status for you <@{context.user_id}> ... standby")


@app.message(
    re.compile("bounce port", re.I),
    middleware=[AsyncSlackScimRBAC(groups={"ChatOps-foo"})],
)
async def app_bounce_port(request: BoltRequest, context: BoltContext, say: Say):
    await say(f"bouncing port for you <@{context.user_id}> ... standby")


# -----------------------------------------------------------------------
# Unhandled messages
# -----------------------------------------------------------------------


@app.event("message")
async def handle_message_events(body, logger):
    logger.info(json.dumps(body, indent=3))
