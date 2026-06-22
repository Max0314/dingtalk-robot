# Permissions And Owners

Use this reference when the user asks who needs to configure DingTalk, or when implementation is blocked by missing permissions.

## Permission Roles

Typical owners:

- DingTalk application administrator: creates/configures enterprise internal application, app credentials, robot capability, callback URL, app visibility.
- System owner/developer: implements callback route, stores config, deploys service, exposes recent event query.
- Business/admin user: confirms target groups, preview/formal separation, command approvers.
- Operations/platform owner: configures HTTPS domain, reverse proxy, environment variables, and deployment secrets.

## Ask For These Values

If missing after code inspection, ask for:

```text
1. DingTalk enterprise app AppKey/AppSecret config method or owner.
2. Public callback domain/service prefix.
3. Preview groups, formal groups, and approver list.
```

Do not ask for the raw `AppSecret` in chat if it can be configured directly in the deployment environment.

## Handoff Template

When the developer needs another admin to configure DingTalk, provide this:

```text
Please help configure a DingTalk enterprise internal application robot:
- System name:
- Robot purpose:
- Callback URL:
- Required capabilities: group message send, @robot callback
- Preview/test groups:
- Formal groups:
- Need message template/msgKey:
- Technical contact:

After setup, configure AppKey/AppSecret in the deployment environment and add the robot to a test group. We will send @robot help to discover openConversationId and robotCode.
```

## Security Rules

- Never paste app secret into source code or screenshots.
- Avoid exposing raw callback payloads to non-admin pages.
- Only configured approvers can trigger formal sends, cancellation, recall, or other business mutations.
- Keep callback public only because DingTalk requires it; every business action still needs authorization.
