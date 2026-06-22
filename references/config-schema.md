# Configuration Schema

Use this reference when designing persistent configuration for a DingTalk robot workflow.

## Recommended JSON Shape

```json
{
  "enabled": true,
  "previewGroupTargets": [
    {
      "name": "AI应用开发组",
      "openConversationId": "cid...",
      "robotCode": "ding...",
      "enabled": true
    }
  ],
  "formalGroupTargets": [
    {
      "name": "大模型技术应用研究-D24/1031-01009-80031",
      "openConversationId": "cid...",
      "robotCode": "ding...",
      "enabled": true
    }
  ],
  "approverTargets": [
    {
      "name": "陈鹏列",
      "userId": "01115324500438248944",
      "enabled": true
    }
  ],
  "approvalCommandScope": "any_configured_group",
  "confirmSendTarget": "formal",
  "sendGroupImages": false
}
```

## Compatibility Guidance

If migrating an older system, normalize legacy names:

- `testGroupTargets` -> `previewGroupTargets`
- `groupTargets` -> `formalGroupTargets`
- `confirmTargets` -> `approverTargets`
- `testMode` should not decide formal confirmation behavior

Confirmation commands should send to `formalGroupTargets` when `confirmSendTarget` is `"formal"`.

## Textarea Format

For simple admin pages, support a line-based format:

```text
群名,openConversationId,robotCode,enabled
```

For approvers:

```text
姓名,userId,enabled
```

Parse `enabled` as true unless it is explicitly `false`, `0`, `no`, `否`, or `停用`.

## Target Selection Rules

- Preview commands send to the current group or `previewGroupTargets`, depending on product design.
- Formal send commands should use `formalGroupTargets`.
- Sensitive commands are accepted only from enabled approvers.
- If `approvalCommandScope` is `any_configured_group`, accept from preview or formal groups.
- If it is `formal_only`, accept only from formal groups.

## Validation

Reject or warn for:

- missing `openConversationId`
- missing `robotCode`
- duplicate group/robot pairs
- enabled approver without `userId`
- formal send enabled with no formal group
