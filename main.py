import os
import requests
import random

NTFY_TOPIC = os.getenv("NTFY_TOPIC")  # e.g., your-phone-topic
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PROMPT = """
Give me a concise algorithm description, preferably machine learning, but any kind of optimization, search etc. algorithm whether its advanced or simple.
Include:
1. Name
2. Purpose
3. Web link with explanation (preferably WikiPedia)
4. Pseudocode or key steps (short)
5. Real-world applications
Format it in max 1000 characters.
"""
def fetch_algorithm():
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT}
                ]
            }
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    content = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    return content

def send_ntfy_notification(message):
    requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=message.encode("utf-8"))

def main():
    algo = fetch_algorithm()
    send_ntfy_notification(algo)

if __name__ == "__main__":
    main()
