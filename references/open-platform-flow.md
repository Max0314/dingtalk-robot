# Open Platform State Flow

Use this reference before telling the user what to do in DingTalk Open Platform. Do not assume the user lacks permissions.

## Three Paths

Classify the user's situation:

1. **Self-service access**
   - User can enter DingTalk Open Platform and create or modify enterprise internal applications.
   - Provide step-by-step self-service setup.

2. **Existing application**
   - User already has Client ID/AppKey, AgentId, robot, or an application screenshot.
   - Treat this as the default if the user provides application IDs.
   - Run a missing-configuration checklist instead of asking them to find an admin.

3. **No permission / escalation**
   - User cannot access Open Platform or cannot modify the application.
   - Provide the admin request template from `permissions-and-owners.md`.

## How To Ask

Ask only when the state is unclear:

```text
You may already have enough DingTalk permissions. Which state matches you?
1. I can create or modify the DingTalk internal application myself.
2. I already have an application/robot and need to check what is missing.
3. I do not have permission and need an admin to configure it.
```

If the user has already provided Client ID, AppKey, AgentId, or robot screenshots, do not ask this question first. Continue with the existing-application checklist.

## Existing Application Checklist

When an application exists, check:

- Client ID/AppKey exists.
- Client Secret/AppSecret will be stored in the backend environment, not chat or Git.
- Robot capability is enabled.
- HTTP callback/receive mode is enabled if @ commands are needed.
- Callback URL is known and reachable.
- The robot can be added to the target test group.
- Required message template/msgKey exists if using interactive cards or template messages.
- A first `@robot help` callback can be recorded to discover `openConversationId`, `robotCode`, and `senderId`.

## Self-Service Setup Checklist

When the user has permissions:

1. Create or open an enterprise internal application.
2. Enable robot capability.
3. Enable HTTP receive/callback mode if commands are required.
4. Configure callback URL after the backend route exists.
5. Configure application visibility.
6. Store Client ID/AppKey and Client Secret/AppSecret in backend secrets.
7. Add the robot to a test group.
8. Send `@robot help` and confirm the backend records an event.

## Escalation Checklist

Use escalation only after confirming the user cannot do the setup. Include:

- system name
- purpose
- callback URL
- required robot capabilities
- test/formal groups
- message template/msgKey requirement
- technical contact
