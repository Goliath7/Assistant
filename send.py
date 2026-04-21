import os
from pathlib import Path

import telebot


def resolve_chat_id(bot: telebot.TeleBot) -> int:
    updates = bot.get_updates()
    if not updates:
        raise RuntimeError(
            "No updates found for this bot. Send at least one message to the bot first."
        )

    for update in reversed(updates):
        if update.message and update.message.chat and update.message.chat.id:
            return int(update.message.chat.id)

        if update.edited_message and update.edited_message.chat and update.edited_message.chat.id:
            return int(update.edited_message.chat.id)

        if update.callback_query and update.callback_query.message and update.callback_query.message.chat:
            return int(update.callback_query.message.chat.id)

    raise RuntimeError("Could not resolve chat_id from bot updates.")


def main() -> None:
    bot_token = "8738352631:AAFI-Tj5_ovG_uZ7XENHBux9AVZkO_wYzfg".strip()
    message = os.environ.get("MESSAGE", "").strip()

    if not message:
        message = Path("message.txt").read_text(encoding="utf-8").strip()

    if not message:
        raise ValueError("Message is empty")

    bot = telebot.TeleBot(bot_token)
    me = bot.get_me()
    print(f"Bot connected: @{me.username}")

    chat_id = resolve_chat_id(bot)
    print("Resolved chat_id:", chat_id)

    result = bot.send_message(chat_id, message)
    print("Sent message id:", result.message_id)


if __name__ == "__main__":
    main()
