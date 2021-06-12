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
    pass


@app.error
async def on_app_exception(error: Exception, request: Request):
    await on_app_specific_exc(error, request)


@on_app_specific_exc.register(SlackRBACPermissionError)
async def on_app_rbac_err(error: SlackRBACPermissionError, request: Request):
    context = request.context
    say = context["say"]
    await say(
        f"Oh no <@{context.user_id}>, you are not allowed to run that command!\n"
        f'You need to be on one of these groups: {", ".join(error.members)}'
    )
