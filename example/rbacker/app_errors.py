from functools import singledispatch


# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from slack_bolt.async_app import AsyncBoltRequest as Request
from slack_rbac import SlackRBACPermissionError

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from .app_data import app

# -----------------------------------------------------------------------------
#
#                                 CODE BEBINS
#
# -----------------------------------------------------------------------------


@singledispatch
async def on_app_specific_exc(error: Exception, request: Request):
    """single dispatch used to multiplex exection types"""
    pass


@app.error
async def on_app_exception(error: Exception, request: Request):
    """Slack-Bolt exception handler"""
    # use the per-exception type multiplexing
    await on_app_specific_exc(error, request)


@on_app_specific_exc.register(SlackRBACPermissionError)
async def on_app_rbac_err(error: SlackRBACPermissionError, request: Request):
    """
    When the Slack-RBAC check fails this exception handler is called.  You can
    then present any message/UI back to the User to indicate this condition.

    In this example, just send back a message.

    Parameters
    ----------
    error: SlackRBACPermissionError instance
    request: Slack-Bolt request instance
    """
    context = request.context
    say = context["say"]
    await say(
        f":fire: Oh no <@{context.user_id}>, you are not allowed to run that command!\n"
        f'You need to be on one of these groups: {", ".join(error.groups)}'
    )
