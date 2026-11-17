# Dialogue Examples

Use these examples to guide first-time users. Keep responses staged and concrete.

## Example 1: User Asks For Guidance On A Frontend Repo

User:

```text
Use Neonet DingTalk Robot to add DingTalk robot capability to ai_code_review_web. Please guide me.
```

Better response:

```text
I first checked the project boundary.

Inferred project profile:
- This repo is a static/frontend project.
- It can show configuration, recent robot events, and trigger notification actions.
- It cannot safely store Client Secret/AppSecret.
- It cannot receive DingTalk callbacks by itself unless there is a backend route behind the same domain.

Recommended robot type: DingTalk enterprise internal application robot.

Next decisions before implementation:
1. Where is the backend repo/service that should receive callbacks?
2. What public domain/API prefix will that backend use?
3. Should the robot only send notifications, or also support @ commands such as help/status/confirm?

You do not need to send Client Secret in chat. The real value should go into backend environment variables.
```

## Example 2: User Provides Existing Application Credentials

User:

```text
I already have AgentId, Client ID, and Client Secret. Do you need these?
```

Better response:

```text
You already have an existing DingTalk application, so we do not need to start by finding an admin.

Field meanings:
- Client ID/AppKey: used by the backend to get DingTalk access tokens.
- Client Secret/AppSecret: backend secret only. Do not put it in frontend code or Git.
- AgentId: application identity; keep it for app-level capabilities, although group robot send may mainly use robotCode + openConversationId.
- robotCode: identifies the robot; usually obtained from robot callback events.
- openConversationId: identifies the group; obtained after the robot is added to a group and someone sends @robot help.

If the Client Secret was pasted into chat, rotate it before production and store the new value only in server environment variables.

What I need next is not the secret value. I need:
1. Backend repo/path or service owner.
2. Backend public callback domain and API prefix.
3. Whether @ commands are required.
```

## Example 3: User Has Open Platform Access

User:

```text
I can configure DingTalk Open Platform myself. What should I do?
```

Better response:

```text
Good. Use the self-service path.

After I add the backend callback route, configure DingTalk Open Platform like this:
1. Open the enterprise internal application.
2. Enable robot capability.
3. Enable HTTP receive/callback mode.
4. Fill callback URL: https://<domain>/<prefix>/api/dingtalk/robot/callback
5. Store Client ID and Client Secret in backend environment variables.
6. Add the robot to a test group.
7. Send @robot help in the test group.
8. Check the system's recent robot events for openConversationId, robotCode, and senderId.

Do not enter openConversationId manually before the callback event exists; it is discovered from the group callback.
```

## Example 4: User Has No Permission

User:

```text
I cannot access DingTalk Open Platform.
```

Better response:

```text
Then use the escalation path. Send this to the DingTalk application owner:

Please configure a DingTalk enterprise internal application robot:
- System name:
- Robot purpose:
- Callback URL:
- Required capabilities: group message send and @robot callback
- Preview/test groups:
- Formal groups:
- Need message template/msgKey:
- Technical contact:

After they add the robot to a test group, send @robot help in that group so the backend can record openConversationId and robotCode.
```

## Anti-Patterns

Avoid:

- Starting with "find an administrator" before checking whether the user has access.
- Dumping all backend APIs, frontend changes, config JSON, and open-platform steps in one long first answer.
- Asking the user to paste Client Secret into chat.
- Treating a frontend repo as if it can receive DingTalk callbacks or store secrets.
- Asking for openConversationId before explaining that it is discovered through callback events.
