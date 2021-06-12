import re
import json

# from slack_bolt.request import BoltRequest
from slack_bolt.context import BoltContext
from slack_bolt.async_app import AsyncSay as Say


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


# -----------------------------------------------------------------------
# Unhandled messages
# -----------------------------------------------------------------------


@app.event("message")
async def handle_message_events(body, logger):
    logger.info(json.dumps(body, indent=3))
