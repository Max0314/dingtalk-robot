---
name: neonet-dingtalk-robot
description: Implement Neonet DingTalk enterprise internal application robot integrations in internal systems. Use when adding group robot message sending, callback event capture, openConversationId/robotCode discovery, @-command handling, approvals, test/formal group push flows, or when guiding developers through DingTalk open-platform setup for Python/FastAPI or other service stacks.
---

# Neonet DingTalk Robot

Use this skill to add DingTalk group robot capabilities to an internal system without rediscovering the DingTalk callback and group-message APIs. Prefer the DingTalk enterprise internal application robot path unless the user explicitly requests a simple custom webhook robot.

## Core Workflow

1. Inspect the target project before asking questions. Identify the stack, routing style, auth middleware, config system, storage layer, deployment path, and existing DingTalk utilities.
2. Present a short inferred project profile for user confirmation. Ask at most 3 blocking questions only when code inspection cannot determine a safe path.
3. Default to an enterprise internal application robot. Only switch to a custom webhook robot if the user asks for simple one-way notification and no @-command callback.
4. Decide the required business capabilities: outbound messages only, callback event capture, @ commands, admin approvals, preview/formal group separation, recall, image/card messages, and send logs.
5. Load the relevant reference:
   - Guided intake and inferred project profile: `references/intake-checklist.md`
   - Robot type decision and default recommendation: `references/robot-type-decision.md`
   - DingTalk open-platform setup: `references/dingtalk-open-platform-setup.md`
   - FastAPI/Python integration: `references/fastapi-integration.md`
   - Callback fields and ID discovery: `references/callback-payload.md`
   - Group/admin configuration shape: `references/config-schema.md`
   - Command parsing and approval flows: `references/command-router.md`
   - Permissions, owners, and escalation: `references/permissions-and-owners.md`
   - Verification and failure analysis: `references/testing-troubleshooting.md`
6. Reuse the templates under `assets/fastapi/` when the target is Python/FastAPI. Copy them with `scripts/scaffold_fastapi.py` or adapt them manually. For other stacks, implement the same contracts from the references in the local framework style.
7. Keep secrets in the target project's existing environment/config mechanism. Never hard-code DingTalk app keys, app secrets, tokens, robot codes, group IDs, or user IDs in committed code.
8. Add tests for command parsing, permission checks, target selection, and missing ID failure modes.

## Integration Rules

- `openConversationId` is discovered from a robot callback. It is not visible in the DingTalk UI.
- `robotCode` must be stored together with its `openConversationId`; treat the pair as the target identity.
- The robot callback route is usually public so DingTalk can call it, but sensitive commands must be authorized by `senderId` and configured group allowlists.
- Store recent callback events so admins can copy group IDs and approver IDs from the system UI or an API.
- For production flows, separate preview/test groups from formal groups. Confirmation commands should always send to formal groups, not depend on a generic `testMode`.
- Log outbound sends and the returned `processQueryKey`; recall only works when this key was captured and DingTalk still allows recall.
- Prefer a small command router with synonyms over many ad hoc `if text contains ...` branches.
- Do not make the user fill every technical detail up front. Infer project conditions from the repository, then ask the user to confirm the inferred plan.
- Include a DingTalk open-platform checklist in the final handoff whenever the integration needs callback or group-message capabilities.

## Recommended Deliverables

For a full integration, produce:

- A DingTalk robot client module for access token, group send, recall, and callback normalization.
- A callback route such as `POST /api/dingtalk/robot/callback`.
- A recent events route for admins, such as `GET /api/dingtalk/robot/events`.
- Tables or equivalent storage for callback events and send logs.
- Config entries for preview groups, formal groups, approvers, and command scope.
- A short admin workflow: add robot to group, @ robot once, copy group ID from recent events, save config, send test message.
- A DingTalk open-platform setup checklist with the callback URL, required app credentials, required robot capability, and permission owner.

## Template Assets

- `assets/fastapi/dingtalk_robot.py`: generic DingTalk robot client helpers.
- `assets/fastapi/robot_routes.py`: FastAPI route skeleton.
- `assets/fastapi/robot_tables.sql`: MySQL table templates for events and send logs.
- `assets/fastapi/robot_config_example.json`: recommended config shape.

Use `scripts/scaffold_fastapi.py --target <repo> --package app.integrations.dingtalk_robot` to copy the FastAPI template files into a target repo. Review and adapt imports before committing.

## Validation Checklist

- `@机器人 help` creates a callback event and returns a help message.
- Recent events show `conversationTitle`, `openConversationId`, `robotCode`, `senderId`, message text, and status.
- Sending to a configured group succeeds and stores `processQueryKey`.
- Missing `openConversationId` or `robotCode` fails with a clear error.
- Non-admin users cannot trigger sensitive commands.
- Commands from unconfigured groups are ignored or rejected according to the requested flow.
