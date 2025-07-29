import os
import requests

NTFY_TOPIC = os.getenv("NTFY_TOPIC")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SENT_FILE = "sent_algorithms.txt"

def load_sent_algorithms():
    if not os.path.exists(SENT_FILE):
        return []
    with open(SENT_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def save_algorithm_name(name):
    with open(SENT_FILE, "a") as f:
        f.write(f"{name}\n")

def fetch_algorithm(avoid_list):
    avoid_str = ", ".join(avoid_list[-20:])  # only last 20 to keep prompt short
    prompt = f"""
Generate a concise and original description of an algorithm, with a bias toward artificial intelligence or optimization. You may also draw from other domains such as cryptography, distributed systems, computer graphics, or information retrieval.

Avoid these algorithms: {avoid_str}

Your response must include:
1. **Name** of the algorithm (first line)
2. A 1–2 sentence **purpose/overview**
3. The **key steps or pseudocode** (brief)
4. 1–2 **real-world applications**
5. A **Wikipedia link** (if available) for further reading

Do not use markdown formatting. Keep the total response under 2000 characters. Use clear, professional language suitable for developers and technically curious readers.
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    content = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    return "NEW ALGORITHM DROPPED ⚡\n" + content

def extract_algorithm_name(text):
    # Assume first line is the name
    return text.strip().splitlines()[0].replace("**", "").strip()

def send_ntfy_notification(message):
    requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=message.encode("utf-8"))

def main():
    sent = load_sent_algorithms()
    for _ in range(3):  # Try up to 3 times to avoid repeats
        algo = fetch_algorithm(sent)
        name = extract_algorithm_name(algo)
        if name not in sent:
            save_algorithm_name(name)
            send_ntfy_notification(algo)
            break
    else:
        send_ntfy_notification("⚠️ Could not generate a new, unique algorithm.")

if __name__ == "__main__":
    main()
