# DingTalk Open Platform Setup

Use this reference whenever the integration requires enterprise internal application robot setup.

## Required Open Platform Operations

Ask the DingTalk application owner/admin to complete these steps:

1. Enter DingTalk Open Platform and open the enterprise internal application.
2. Confirm or create the application used by the target system.
3. Copy `AppKey` and `AppSecret` into the target system's secret/config mechanism.
4. Enable robot-related capability for the application.
5. Enable robot HTTP receive/callback mode if `@机器人` commands are required.
6. Configure the callback URL, for example:

```text
https://<domain>/<service-prefix>/api/dingtalk/robot/callback
```

7. Ensure the callback URL is public HTTPS and not blocked by login middleware.
8. Configure application visibility/scope so the robot can be added to the target groups.
9. If using interactive cards or template messages, create or confirm the required `msgKey`.
10. Add the robot to a test group and send `@机器人 help` to generate the first callback event.

## Information The Developer Should Provide To The DingTalk Admin

```text
Application/system name:
Robot purpose:
Callback URL:
Preview/test groups:
Formal groups:
Need @ commands:
Need message template/msgKey:
Launch time:
Technical contact:
```

## Values The Application Must Store

Store as secrets/config, not source code:

- `DINGTALK_APP_KEY`
- `DINGTALK_APP_SECRET`

Store group and approver config in a database/config table/admin page:

- `openConversationId`
- `robotCode`
- group display name
- approver `senderId` or staff ID

## Callback URL Checks

Before telling the admin the URL, verify:

- route exists in the service
- reverse proxy forwards the path
- base path is included, such as `/bi_center`
- public HTTPS certificate is valid
- unauthenticated DingTalk requests can reach only the callback route

## When Permissions Are Missing

If the developer lacks DingTalk Open Platform permissions, ask for help from the enterprise DingTalk application administrator or platform owner. Provide the information block above instead of asking the developer to guess app settings.
