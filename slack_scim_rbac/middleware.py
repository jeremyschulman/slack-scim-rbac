# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import Callable, Awaitable, Set, Optional, Any
import os
import inspect

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse

from slack_sdk.scim.async_client import AsyncSCIMClient
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.kwargs_injection.async_utils import build_async_required_kwargs
from slack_bolt.logger import get_bolt_app_logger


_develop_scim_user_id = os.environ["SLACK_DEVELOP_SCIM_USER"]
_scim_token = os.environ["SLACK_SCIM_TOKEN"]


class AsyncSlackScimRBAC(AsyncMiddleware):
    def __init__(
        self,
        *,
        app_name: str,
        groups: Set[str],
        error_response: Optional[Callable[..., Awaitable[Any]]] = None,
    ):
        if error_response and not inspect.iscoroutinefunction(error_response):
            raise ValueError("error_response must be an async function")

        self.app_name = app_name
        self._error_response = error_response
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
        scim_resp = await AsyncSCIMClient(token=_scim_token).read_user(id=user_id)
        user_groups = context["scim_groups"] = {
            g.display for g in scim_resp.user.groups
        }

        if not self.is_member(user_groups):
            await context["ack"]()
            if not self._error_response:
                err_resp = self.error_response(req=req)
            else:
                func = self._error_response

                err_resp = self._error_response(
                    **build_async_required_kwargs(
                        logger=get_bolt_app_logger(self.app_name, func),
                        required_arg_names=inspect.getfullargspec(func).args,
                        request=req,
                        response=resp,
                        this_func=self._error_response,
                    )
                )

            await err_resp
            return BoltResponse(status=200, body="")

        return await next()
