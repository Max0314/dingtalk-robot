# Testing And Troubleshooting

Use this reference before finishing a DingTalk robot integration.

## Manual Test Flow

1. Add the robot to a test group.
2. Send `@机器人 help`.
3. Confirm a callback event was stored.
4. Copy `openConversationId`, `robotCode`, and approver `senderId` from recent events.
5. Configure the test group and approver.
6. Send a preview/test message to the group.
7. Test a denied sensitive command from a non-approver.
8. Test an approved command from an approver.
9. Check send logs and returned `processQueryKey`.

## Automated Tests

Add tests for:

- `parse_robot_callback_event` handles missing fields.
- `parse_command` maps synonyms correctly.
- missing group ID or robot code returns a clear error.
- configured group allowlist works.
- approver allowlist blocks non-admin users.
- formal send target selection ignores legacy `testMode`.

## Common Failures

### No callback event appears

- Robot is not in HTTP receive mode.
- Callback URL is not reachable from DingTalk.
- Login/auth middleware blocks the callback path.
- Reverse proxy path prefix is wrong.
- The message did not @ the robot.

### `openConversationId` is empty

- The payload is from a different DingTalk event type.
- The field name differs; inspect raw payload JSON.
- The callback storage truncated or filtered the field.

### Group send fails

- App key/secret are wrong or token fetch fails.
- `robotCode` does not match the group robot.
- `openConversationId` was copied from another group.
- Message template `msgKey` is not configured for that robot.
- `msgParam` is not JSON-encoded as DingTalk expects.

### Command has no response

- The group is not in the configured allowlist.
- The parser did not recognize a synonym.
- Sender is not an approver.
- Callback route stores events but does not call the command router.

## Production Checks

- Confirm no secrets are committed.
- Confirm callback route is intentionally public but command actions are protected.
- Confirm logs do not expose direct personal contact/payment identifiers.
- Confirm failures are visible in logs or admin UI.
