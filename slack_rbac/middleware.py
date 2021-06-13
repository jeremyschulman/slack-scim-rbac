# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import Callable, Awaitable, Set
import os

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse

from slack_sdk.scim.async_client import AsyncSCIMClient
from slack_bolt.middleware.async_middleware import AsyncMiddleware

_develop_scim_user_id = os.environ["SLACK_DEVELOP_SCIM_USER"]
_scim_token = os.environ["SLACK_SCIM_TOKEN"]


class AsyncSlackScimRBAC(AsyncMiddleware):
    def __init__(self, *, groups: Set[str]):
        self.scim_groups = groups

    def is_member(self, user_groups: Set):
        """return True if the user is a member of any of the required groups"""

        return user_groups & self.scim_groups

    async def error_response(self, req: AsyncBoltRequest):
        """Send an error indication to the User"""

        context = req.context
        say = context["say"]
        await say(
            f":octagonal_sign: I'm sorry <@{context.user_id}>, you are not authorized."
        )

    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],  # noqa
    ) -> BoltResponse:

        context = req.context
        user_id = _develop_scim_user_id or context.user_id
        resp = await AsyncSCIMClient(token=_scim_token).read_user(id=user_id)
        user_groups = context["scim_groups"] = {g.display for g in resp.user.groups}

        if not self.is_member(user_groups):
            await context["ack"]()
            await self.error_response(req)
            return BoltResponse(status=200, body="")

        return await next()
