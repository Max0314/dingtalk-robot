# Intake Checklist

Use this reference at the start of an integration. Do not ask the user to fill this whole checklist. Inspect the repository first, then present a short inferred profile for confirmation.

## Repository Signals To Inspect

Look for:

- framework and entrypoint: FastAPI, Flask, Django, Express, NestJS, Spring Boot, Go, etc.
- route registration pattern and API prefix
- auth middleware and public-route whitelist
- config mechanism: `.env`, Pydantic settings, Spring properties, config center, Kubernetes secrets
- database and migration style
- existing DingTalk, notification, webhook, or message utilities
- background job/scheduler style if the robot sends timed messages
- admin UI conventions if group/approver config needs a page
- deployment base path and public HTTPS domain

## Inferred Profile To Show The User

After inspection, summarize:

```text
Inferred project profile:
- Stack:
- Suggested API prefix/callback path:
- Config mechanism:
- Storage mechanism:
- Auth/login middleware:
- Recommended robot type: enterprise internal application robot
- Suggested capabilities:

Please confirm whether this profile is correct. If there is no objection, proceed with this plan.
```

If the user already clearly asked for implementation and the inferred path is safe, proceed after the summary without blocking. Ask only if a decision changes architecture or security.

## Questions Only When Needed

Ask at most 3 blocking questions, chosen from:

1. The robot should only send notifications, or also receive `@robot` commands?
2. Which groups are preview/test groups and which are formal groups?
3. Who are the approvers/admins for sensitive commands?
4. What public callback URL should DingTalk call after deployment?
5. Does the target service already have DingTalk `AppKey/AppSecret` configuration?

## Default Assumptions

- Recommend enterprise internal application robot.
- Support group ID discovery through recent callback events.
- Separate preview/test groups and formal groups when messages can affect business workflow.
- Store send logs if messages may need audit, retry, or recall.
- Keep callback route public but protect actions by group allowlist and approver `senderId`.
