# FastAPI Integration

Use this reference when the target service is Python/FastAPI or has a similar router/service layout.

## Recommended Shape

Add three layers:

1. `dingtalk_robot.py`: API client and payload normalization. It should not know business commands.
2. Route module: `POST /api/dingtalk/robot/callback` and optional admin routes.
3. Service layer: command routing, config lookup, event storage, send logs, and business actions.

Keep the callback route public for DingTalk. Put all authorization in the service layer.

## Environment

Use the target project's config mechanism. The template expects these names, but adapt to local conventions:

```text
DINGTALK_APP_KEY
DINGTALK_APP_SECRET
DINGTALK_ROBOT_CALLBACK_SECRET   optional, if signature validation is implemented
```

Do not commit real values.

## Route Pattern

```python
@router.post("/dingtalk/robot/callback")
async def dingtalk_robot_callback(request: Request) -> dict:
    try:
        payload = await request.json()
    except Exception:
        payload = {}
    service.record_dingtalk_robot_event(payload if isinstance(payload, dict) else {})
    return {"success": True}
```

The route should return success quickly. Business failures should be logged and optionally replied to the group; they should not cause DingTalk retries unless retry is desired.

## Storage

At minimum, persist callback events:

- conversation ID/title/type
- sender nick and sender ID
- robot code
- message text
- parsed command
- handle status
- response text
- raw payload JSON
- created time

Persist send logs when messages may need audit, retry, or recall:

- target group ID and robot code
- message type/key
- `processQueryKey`
- send status and error
- business object ID if applicable

Use `assets/fastapi/robot_tables.sql` as a MySQL starting point.

## Admin UI/API

Expose a recent-event API for admins:

```text
GET /api/dingtalk/robot/events?limit=20
```

It should return `openConversationId`, `conversationTitle`, `robotCode`, `senderId`, `senderNick`, message text, status, and created time. This is the easiest way to discover group IDs.

## Implementation Steps

1. Copy `assets/fastapi/dingtalk_robot.py`.
2. Copy or adapt `assets/fastapi/robot_routes.py`.
3. Create event/send-log tables or equivalent storage.
4. Add config fields from `references/config-schema.md`.
5. Add a command router from `references/command-router.md`.
6. Add tests:
   - callback normalization
   - group discovery
   - missing group/robot code
   - admin command authorization
   - successful group send

## Common Adaptations

- If the project already has a DingTalk access-token client, reuse it instead of adding another cache.
- If the project has global login middleware, whitelist only the callback route, not admin query routes.
- If the project does not use MySQL, map the SQL schema to the local database or config store.
