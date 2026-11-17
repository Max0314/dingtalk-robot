"""FastAPI route skeleton for DingTalk robot callbacks.

Adapt imports and service wiring to the target project.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

from .dingtalk_robot import parse_robot_callback_event


router = APIRouter(prefix="/api", tags=["dingtalk-robot"])


class RobotService:
    """Replace this with the target project's real service class."""

    def record_dingtalk_robot_event(self, payload: dict[str, Any]) -> dict[str, Any]:
        event = parse_robot_callback_event(payload)
        # TODO: store event, parse command, authorize, and optionally reply.
        return {**event, "handleStatus": "ignored"}

    def get_dingtalk_robot_events(self, *, limit: int) -> dict[str, Any]:
        # TODO: load recent stored events. Restrict this route to admins.
        return {"events": [], "limit": limit}


def get_robot_service() -> RobotService:
    # TODO: replace with the target app's service dependency.
    return RobotService()


@router.post("/dingtalk/robot/callback")
async def dingtalk_robot_callback(request: Request) -> dict[str, bool]:
    # Public endpoint for DingTalk HTTP receive mode. Keep it quick and move
    # authorization into the command handler.
    try:
        payload = await request.json()
    except Exception:
        payload = {}
    try:
        get_robot_service().record_dingtalk_robot_event(payload if isinstance(payload, dict) else {})
    except Exception:
        # Log in the target project. Returning success avoids noisy retries for
        # non-critical command failures.
        pass
    return {"success": True}


@router.get("/dingtalk/robot/events")
def dingtalk_robot_events(limit: int = Query(default=20, ge=1, le=50)) -> dict[str, Any]:
    # TODO: require admin permission before returning sender/group IDs.
    try:
        return get_robot_service().get_dingtalk_robot_events(limit=limit)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
