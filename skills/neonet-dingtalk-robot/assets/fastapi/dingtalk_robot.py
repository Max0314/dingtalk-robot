"""Reusable DingTalk group robot helpers.

Copy this file into the target service and wire secrets through that service's
configuration system. Do not commit real app keys, app secrets, robot codes, or
conversation IDs.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


_TOKEN_CACHE: dict[str, Any] = {"access_token": "", "expires_at": 0.0}


class DingTalkRobotError(RuntimeError):
    pass


def _normalize_text(value: Any) -> str:
    return str(value or "").strip()


def _json_post(url: str, *, headers: dict[str, str] | None = None, payload: dict[str, Any] | None = None, timeout: int = 15) -> dict[str, Any]:
    data = json.dumps(payload or {}, ensure_ascii=False).encode("utf-8")
    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise DingTalkRobotError(str(exc)) from exc
    try:
        parsed = json.loads(body or "{}")
    except json.JSONDecodeError as exc:
        raise DingTalkRobotError(f"invalid DingTalk JSON response: {body[:300]}") from exc
    if not isinstance(parsed, dict):
        raise DingTalkRobotError("invalid DingTalk response type")
    return parsed


def get_access_token(*, app_key: str | None = None, app_secret: str | None = None) -> str:
    key = _normalize_text(app_key or os.getenv("DINGTALK_APP_KEY"))
    secret = _normalize_text(app_secret or os.getenv("DINGTALK_APP_SECRET"))
    if not key or not secret:
        raise DingTalkRobotError("DingTalk app key or app secret missing")
    now = time.time()
    if _TOKEN_CACHE.get("access_token") and float(_TOKEN_CACHE.get("expires_at") or 0) - now > 120:
        return str(_TOKEN_CACHE["access_token"])
    response = _json_post(
        "https://api.dingtalk.com/v1.0/oauth2/accessToken",
        payload={"appKey": key, "appSecret": secret},
        timeout=10,
    )
    token = _normalize_text(response.get("accessToken"))
    if not token:
        raise DingTalkRobotError(str(response.get("message") or response))
    expires_in = int(response.get("expireIn") or 7200)
    _TOKEN_CACHE.update({"access_token": token, "expires_at": now + max(300, expires_in)})
    return token


def send_robot_group_message(
    *,
    open_conversation_id: str,
    robot_code: str,
    msg_key: str,
    msg_param: dict[str, Any],
    app_key: str | None = None,
    app_secret: str | None = None,
) -> dict[str, Any]:
    conversation_id = _normalize_text(open_conversation_id)
    robot_code_text = _normalize_text(robot_code)
    if not conversation_id or not robot_code_text:
        return {"sent": False, "error": "robot conversation or robot code missing", "processQueryKey": ""}
    token = get_access_token(app_key=app_key, app_secret=app_secret)
    response = _json_post(
        "https://api.dingtalk.com/v1.0/robot/groupMessages/send",
        headers={"x-acs-dingtalk-access-token": token},
        payload={
            "robotCode": robot_code_text,
            "openConversationId": conversation_id,
            "msgKey": _normalize_text(msg_key),
            "msgParam": json.dumps(msg_param or {}, ensure_ascii=False),
        },
    )
    if response.get("code") or response.get("message"):
        return {"sent": False, "error": str(response.get("message") or response), "processQueryKey": ""}
    return {
        "sent": True,
        "error": "",
        "processQueryKey": _normalize_text(response.get("processQueryKey") or response.get("taskId") or response.get("task_id")),
        "raw": response,
    }


def recall_robot_group_messages(
    *,
    open_conversation_id: str,
    robot_code: str,
    process_query_keys: Iterable[str] | str,
    app_key: str | None = None,
    app_secret: str | None = None,
) -> dict[str, Any]:
    keys = [_normalize_text(item) for item in ([process_query_keys] if isinstance(process_query_keys, str) else process_query_keys)]
    keys = [item for item in keys if item]
    conversation_id = _normalize_text(open_conversation_id)
    robot_code_text = _normalize_text(robot_code)
    if not conversation_id or not robot_code_text:
        return {"recalled": False, "error": "robot conversation or robot code missing"}
    if not keys:
        return {"recalled": False, "error": "process query key missing"}
    token = get_access_token(app_key=app_key, app_secret=app_secret)
    response = _json_post(
        "https://api.dingtalk.com/v1.0/robot/groupMessages/recall",
        headers={"x-acs-dingtalk-access-token": token},
        payload={
            "robotCode": robot_code_text,
            "openConversationId": conversation_id,
            "processQueryKeys": keys,
        },
    )
    if response.get("code") or response.get("message"):
        return {"recalled": False, "error": str(response.get("message") or response)}
    return {"recalled": True, "error": "", "raw": response}


def sender_id_from_payload(payload: dict[str, Any]) -> str:
    for key in ("senderStaffId", "senderId", "senderUserId", "senderUnionId", "userId"):
        value = _normalize_text(payload.get(key))
        if value:
            return value
    sender = payload.get("sender") if isinstance(payload.get("sender"), dict) else {}
    for key in ("staffId", "userId", "unionId", "id"):
        value = _normalize_text(sender.get(key))
        if value:
            return value
    return ""


def parse_robot_callback_event(payload: dict[str, Any] | None) -> dict[str, Any]:
    data = payload if isinstance(payload, dict) else {}
    text = data.get("text") if isinstance(data.get("text"), dict) else {}
    return {
        "openConversationId": _normalize_text(data.get("conversationId")),
        "conversationTitle": _normalize_text(data.get("conversationTitle")),
        "conversationType": _normalize_text(data.get("conversationType")),
        "senderNick": _normalize_text(data.get("senderNick")),
        "senderId": sender_id_from_payload(data),
        "robotCode": _normalize_text(data.get("robotCode")),
        "messageText": _normalize_text(text.get("content")),
        "raw": data,
    }


def markdown_param(title: str, text: str) -> dict[str, str]:
    return {"title": _normalize_text(title), "text": str(text or "")}


def text_param(content: str) -> dict[str, str]:
    return {"content": str(content or "")}
