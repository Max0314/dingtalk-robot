# Callback Payload And ID Discovery

Use this reference when implementing robot receive mode or helping admins find `openConversationId`, `robotCode`, and `senderId`.

## Important Fields

DingTalk robot callback payloads commonly include:

```json
{
  "conversationId": "cid...",
  "conversationTitle": "AI应用开发组",
  "conversationType": "2",
  "senderNick": "陈鹏列",
  "senderStaffId": "01115324500438248944",
  "senderId": "$sender-id-or-open-id",
  "robotCode": "ding...",
  "text": {
    "content": " help"
  }
}
```

Field names can vary across DingTalk robot modes. Normalize sender identity by checking likely fields such as:

- `senderStaffId`
- `senderId`
- `senderUnionId`
- `senderUserId`
- `userId`

Prefer the stable corporate user ID/staff ID when present.

## Group Discovery Flow

1. Add the robot to the target group.
2. Send `@机器人 help` or any diagnostic message.
3. The callback event contains:
   - `conversationId` -> store/display as `openConversationId`
   - `conversationTitle`
   - `robotCode`
   - `senderId`
4. Admin copies the row into config:

```text
群名,openConversationId,robotCode,true
```

Example:

```text
大模型技术应用研究-D24/1031-01009-80031,cid9SKRQBZjJizsAK5ZAN9m9A==,dingxiabphfbmktmfd1i,true
```

## Normalization Rules

- Trim leading spaces in `text.content`; DingTalk may include a leading space after @.
- Store raw payload JSON for later debugging.
- Cap stored text lengths to avoid oversized rows.
- Treat empty `conversationId` or `robotCode` as unusable for group replies.
- Do not expose raw payloads to non-admin users.

## Security Notes

The callback endpoint may be public, but do not trust the message:

- Check configured group allowlist before acting.
- Check approver/admin `senderId` before sensitive actions.
- Consider DingTalk signature validation if the deployment has a callback secret and the robot mode supports it.
