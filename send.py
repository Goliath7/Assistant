import os
import requests


def main() -> None:
    bot_token = os.environ["BOT_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    message = os.environ.get("MESSAGE", "Test message from GitHub Actions")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message,
        },
        timeout=20,
    )

    print("Status:", response.status_code)
    print("Response:", response.text)
    response.raise_for_status()


if __name__ == "__main__":
    main()
