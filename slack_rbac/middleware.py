# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

import os

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from slack_sdk.scim.async_client import AsyncSCIMClient
from slack_bolt.async_app import AsyncBoltContext

_develop_scim_user_id = os.environ["SLACK_DEVELOP_SCIM_USER"]
_scim_token = os.environ["SLACK_SCIM_TOKEN"]


async def aio_scim_groups(context: AsyncBoltContext, next):  # noqa
    """
    Obtain the set of SCIM group names associated with the given user in
    context.  These group names are then stored in the context using the key
    'scim_groups'.

    Parameters
    ----------
    context: Slack Bolt context
    next: utility function to chain middleware
    """
    user_id = _develop_scim_user_id or context.user_id
    resp = await AsyncSCIMClient(token=_scim_token).read_user(id=user_id)
    context["scim_groups"] = {g.display for g in resp.user.groups}
    await next()
