from slack_bolt.async_app import AsyncBoltRequest


class SlackRBACPermissionError(Exception):
    def __init__(self, members):
        super(SlackRBACPermissionError, self).__init__()
        self.members = members


def assert_rbac_members(request: AsyncBoltRequest, member_set):
    if not isinstance(member_set, set):
        member_set = set(member_set)

    context = request.context
    if not (context["scim_groups"] & member_set):
        raise SlackRBACPermissionError(member_set)
