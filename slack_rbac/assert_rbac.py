from slack_bolt.async_app import AsyncBoltRequest


class SlackRBACPermissionError(Exception):
    def __init__(self, groups):
        super(SlackRBACPermissionError, self).__init__()
        self.groups = groups


def assert_rbac_membership(request: AsyncBoltRequest, groups):
    if not isinstance(groups, set):
        groups = set(groups)

    context = request.context
    if not (context["scim_groups"] & groups):
        raise SlackRBACPermissionError(groups)
