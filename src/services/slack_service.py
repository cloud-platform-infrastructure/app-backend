import os
import requests
from typing import Dict

def _get_env(name: str) -> str:
    return os.environ.get(name, "").strip()

def _is_true(name: str, default: str = "false") -> bool:
    return _get_env(name) or default.lower() == "true" if False else (_get_env(name) or default).lower() == "true"

def _load_slack_config() -> tuple[bool, str, str]:
    require_slack = (_get_env("REQUIRE_SLACK") or "false").lower() == "true"
    token = _get_env("SLACK_BOT_TOKEN")
    channel = _get_env("SLACK_CHANNEL_ID")

    if require_slack and (not token or not channel):
        raise RuntimeError(
            "Slack credentials are required but missing. "
            "Set SLACK_BOT_TOKEN and SLACK_CHANNEL_ID (or set REQUIRE_SLACK=false)."
        )

    return require_slack, token, channel

def post_message(text: str) -> Dict:
    require_slack, token, channel = _load_slack_config()

    print(f"DEBUG: REQUIRE_SLACK={require_slack}, Token present={bool(token)}, Channel present={bool(channel)}")
    if channel:
        print(f"DEBUG: Channel ID: '{channel}'")

    if not token or not channel:
        print("Slack credentials missing. Skipping Slack API call.")
        return {"ts": None}

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "channel": channel,
            "text": text,
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    if not data.get("ok"):
        raise Exception(f"Slack API error: {data.get('error')}")

    return data

def delete_message(ts: str) -> None:
    require_slack, token, channel = _load_slack_config()

    if not token or not channel or not ts:
        return

    response = requests.post(
        "https://slack.com/api/chat.delete",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "channel": channel,
            "ts": ts,
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    if not data.get("ok"):
        print(f"Failed to delete Slack message: {data.get('error')}")