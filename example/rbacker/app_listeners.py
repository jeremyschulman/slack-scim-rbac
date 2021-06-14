# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

import re
import json

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.models.views import View
from slack_sdk.models.blocks import SectionBlock, MarkdownTextObject as MdText

from slack_bolt.async_app import (
    AsyncBoltContext as Context,
)
from slack_bolt.async_app import AsyncSay as Say
from slack_bolt.context.ack.async_ack import AsyncAck as Ack
from slack_scim_rbac.middleware import AsyncSlackScimRBAC

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from .app_data import app


@app.event("app_mention")
async def app_mention(context: Context, say: Say):
    await say(f"You mentioned me <@{context.user_id}>?")


# -----------------------------------------------------------------------
# Messages to the app in the app specific channel
# -----------------------------------------------------------------------


@app.message(re.compile("hi", re.I))
async def app_say_ohai(context: Context, say: Say):
    await say(f"Ohai <@{context.user_id}>")


@app.message(re.compile("show port", re.I))
async def app_show_port(context: Context, say: Say):
    await say(f"getting port status for you <@{context.user_id}> ... standby")


async def no_your_cant(context: Context, say: Say):
    await say(
        f"Nope, sorry <@{context.user_id}>, you don't have permission to do that."
    )


@app.message(
    re.compile("bounce port", re.I),
    middleware=[
        AsyncSlackScimRBAC(
            app_name=app.name, groups={"ChatOps-bozo"},
            error_response=no_your_cant
        )
    ],
)
async def app_bounce_port(context: Context, say: Say):
    await say(f"bouncing port for you <@{context.user_id}> ... standby")


# -----------------------------------------------------------------------
# Slash commands
# -----------------------------------------------------------------------


async def is_bounce_port_command(command: dict):
    return "bounce port" in command["text"]


async def modal_no_you_cant(client: AsyncWebClient, body, context: Context):
    msg = f"Nope! Sorry <@{context.user_id}> but you cannot do that!"

    view = View(title="Permission Denied!", type="modal", close="Bummer")
    view.blocks = [SectionBlock(text=MdText(text=msg))]
    await client.views_open(trigger_id=body["trigger_id"], view=view)


@app.command(
    command="/rbacker",
    matchers=[is_bounce_port_command],
    middleware=[
        AsyncSlackScimRBAC(
            app_name=app.name,
            groups={"ChatOps-bozo"},
            error_response=modal_no_you_cant,
        )
    ],
)
async def slash_rbacker_bounce_port(ack: Ack, say: Say, context: Context):
    await ack()
    await say(
        f"Already then, <@{context.user_id}>, let's get to bouncing that port for ya!"
    )


# -----------------------------------------------------------------------
# Unhandled messages
# -----------------------------------------------------------------------


@app.event("message")
async def handle_message_events(body, logger):
    logger.info(json.dumps(body, indent=3))


@app.command("/rbacker")
async def handle_some_command(ack, body, logger):
    await ack()
    logger.info(json.dumps(body, indent=3))
