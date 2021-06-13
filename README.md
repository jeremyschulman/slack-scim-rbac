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

```python
@app.message(
    re.compile("bounce port", re.I),
    middleware=[AsyncSlackScimRBAC(groups={"ChatOps-foo"})],
)
async def app_bounce_port(request: BoltRequest, context: BoltContext, say: Say):
    await say(f"bouncing port for you <@{context.user_id}> ... standby")
```


# Resources

* [Video: Getting Started with Python Slack-Bolt PyCon 2021](https://www.youtube.com/watch?v=Mlh8BD7xlgE)
* [Article: What is SCIM?](https://www.okta.com/blog/2017/01/what-is-scim/)
