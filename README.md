# Role Based Access Control for Slack-Bolt Apps

Role Based Access Control (RBAC) is a term applied to limiting the
authorization for a specific operation based on the association of a User to a
"role".  For example:

    As an application developer, I want to ensure that only specific Users in a
    given User-Group are allowed to execute the "bounce port" command.

The Slack Platform does not natively support the concept of "User Groups", but
it does support the standard protcol: System for Cross-domain Identity
Management (SCIM).  A method for implemeting RBAC in Slack can be accomlished
using the Slack SCIM API feature.  For example:

    As an IT administrator of Okta, I will create SCIM groups that will designate
    the specific RBAC User-Groups I want to use in Slack.

This `slack-scim-rbac` repository provides a Slack-Bolt _middleware_ class.

As a developer using the SCIM protocol, you must obtain a SCIM Token from your Slack
administrator and export the environment variable `SLACK_SCIM_TOKEN`.

The following code snippet is take from the [example](example/rbacker/app_listeners.py).
In this example the User that entered the "bounce port" message must be a member
of the SCIM group "ChatOps-foo".  If they are not, then an error message is reported
to the User.

```python
from slack_scim_rbac.middleware import AsyncSlackScimRBAC

@app.message(
    re.compile("bounce port", re.I),
    middleware=[AsyncSlackScimRBAC(groups={"ChatOps-foo"})],
)
async def app_bounce_port(request: BoltRequest, context: BoltContext, say: Say):
    await say(f"bouncing port for you <@{context.user_id}> ... standby")
```

# Customizing the Error Response

As a developer you will want to customize the error response to the User.
There are two ways to do this. The first way is to provide an `error_response`
function to middleware addition.  For example this code will trigger a Modal
when the User triggers the `/rbacker` command that contains the text "bounce
port" when they are not part of the "ChatOps-nofuzz" SCIM group.

```python
async def is_bounce_port_command(command: dict):
    return "bounce port" in command["text"]


async def modal_no_you_cant(client: AsyncWebClient, body: dict, context: AsyncBoltContext):
    msg = f"Nope! Sorry <@{context.user_id}> but you cannot do that!"

    view = View(title="Permission Denied!", type="modal", close="Bummer")
    view.blocks = [SectionBlock(text=MarkdownTextObject(text=msg))]
    await client.views_open(trigger_id=body["trigger_id"], view=view)


@app.command(
    command="/rbacker",
    matchers=[is_bounce_port_command],
    middleware=[
        AsyncSlackScimRBAC(
            app_name=app.name,
            groups={"ChatOps-nofuzz"},
            error_response=modal_no_you_cant,
        )
    ],
)
async def slash_rbacker_bounce_port(ack: Ack, say: Say, context: Context):
    await ack()
    await say(
        f"Already then, <@{context.user_id}>, let's get to bouncing that port for ya!"
    )
```

The other approach is to sub-class the `AsyncSlackScimRBAC` class and
overriding the `error_response` method.

# Customizing the RBAC Validation Process

By default the validate process checks the Slack User groups (name) membership
in any of the required group names.  You can override this behavior (for
example if you have a default "admin" group that you want to always allow but
not require in each listener declaration) by sub-classing `AsyncSlackScimRBAC`
and overriding the `is_member` method.

# Limitations

This `slack-scim-rbac` repository implements middleware for asyncio mode only.
A sync implementation should be straightforward, but has not been done since it
is not what I needed.  If you do, please open an issue (or a PR).  Thanks!

# Resources

* [Slack-Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started)
* [Video: Getting Started with Python Slack-Bolt PyCon 2021](https://www.youtube.com/watch?v=Mlh8BD7xlgE)
* [Article: What is SCIM?](https://www.okta.com/blog/2017/01/what-is-scim/)
