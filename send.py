import os
from pathlib import Path

import requests


def resolve_chat_id(bot_token: str) -> int:
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    results = data.get("result", [])
    if not results:
        raise RuntimeError(
            "No updates found for this bot. Send at least one message to the bot first."
        )

    for update in reversed(results):
        message = update.get("message") or update.get("edited_message")
        if message and "chat" in message and "id" in message["chat"]:
            return int(message["chat"]["id"])

        callback_query = update.get("callback_query")
        if callback_query and "message" in callback_query:
            chat = callback_query["message"].get("chat", {})
            if "id" in chat:
                return int(chat["id"])

    raise RuntimeError("Could not resolve chat_id from bot updates.")


def main() -> None:
    bot_token = os.environ["BOT_TOKEN"]
    message = os.environ.get("MESSAGE", "").strip()

    if not message:
        message = Path("message.txt").read_text(encoding="utf-8").strip()

    if not message:
        raise ValueError("Message is empty")

    chat_id = resolve_chat_id(bot_token)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message,
        },
        timeout=20,
    )

    print("Resolved chat_id:", chat_id)
    print("Status:", response.status_code)
    print("Response:", response.text)
    response.raise_for_status()


if __name__ == "__main__":
    main()
