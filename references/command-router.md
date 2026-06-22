# Command Router

Use this reference when the robot must respond to @ commands or approval messages.

## Recommended Commands

Start with a small synonym map:

```text
help: help, 帮助, 指令, 怎么用
status: 状态, 发送状态, 周报状态, 当前状态
preview: 预览, 预览周报, 发送预览, 重新预览
confirm: 确认发送, 同意发送, 可以发送, 正式发送
changes: 需要修改, 修改意见, 退回
cancel: 取消发送, 暂停发送, 不发送
recall: 撤回, 撤回周报, 撤回消息
```

Adapt names to the business domain. Keep the parser deterministic and testable.

## Parsing Rules

- Remove bot mentions if the platform leaves them in the text.
- Trim whitespace and leading punctuation.
- Match exact commands before fuzzy `contains` checks.
- For commands with payloads, support both Chinese and English colon:

```text
需要修改：摘要太泛，需要补充风险
需要修改: 摘要太泛，需要补充风险
```

## Authorization

For every inbound command:

1. Normalize event fields.
2. Store the event.
3. Check whether the group is known/configured.
4. Parse command.
5. For safe commands (`help`, sometimes `status`), reply even if not configured if product wants easier discovery.
6. For sensitive commands (`confirm`, `cancel`, `recall`, business mutations), require:
   - configured group
   - enabled approver `senderId`
   - valid business state

## Reply Style

Replies should be short and actionable:

```text
当前支持：
- help / 帮助：查看指令
- 预览周报：在当前群发送预览
- 确认发送：管理员确认后发送正式群
- 需要修改：修改意见
```

For denied actions, include only the reason needed to fix it:

```text
未执行：你不在确认管理员列表中。请先让管理员在配置页加入 senderId。
```

## State Guards

Before formal sends or destructive actions, check state:

- already sent -> do not resend unless the business explicitly supports retry
- need changes -> block formal send until reset
- missing rendered content or missing target group -> fail clearly
- recall without `processQueryKey` -> explain that recall cannot be attempted
