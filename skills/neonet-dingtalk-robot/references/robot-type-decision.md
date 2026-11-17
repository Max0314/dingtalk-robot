# Robot Type Decision

Use this reference when deciding which DingTalk robot model to implement.

## Default Recommendation

Recommend **enterprise internal application robot** for Neonet internal systems.

Choose this when any of these are needed:

- send group messages through `openConversationId` and `robotCode`
- receive `@机器人` callbacks
- discover `openConversationId`
- handle approval commands such as `确认发送`
- separate preview and formal groups
- identify sender by `senderId`
- keep audit logs and recall messages
- integrate with enterprise app permissions

This is the default path for BI weekly reports and similar internal operational systems.

## Custom Webhook Robot

Only choose a custom webhook robot when the user explicitly wants simple one-way notifications and does not need:

- callback receive mode
- `@机器人` command handling
- sender identity
- admin approval
- group ID discovery
- recall/audit workflows

Custom webhook integrations usually use a webhook URL and optional signing secret. They are simpler but much less suitable for approval workflows.

## How To Explain The Choice

Use concise language:

```text
Recommend the enterprise internal application robot because this flow needs @ commands, sender identity, preview/formal group separation, and approval capability. A custom webhook robot is better for simple one-way notifications only.
```

If the user is unsure, proceed with enterprise internal application robot unless project constraints make it impossible.
