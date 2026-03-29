import os, requests
from flask import Flask, request

app = Flask(__name__)
TOKEN = os.environ["TG_TOKEN"]
MEM_KEY = os.environ["MEM_KEY"]
COLLECTION = "f2008aa3-8b63-4781-bd8f-1168fbf467d2"
BOT_NAME = "Kingmaster_Maxclaw"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    msg = data.get("message") or data.get("edited_message")
    if not msg or not msg.get("text"):
        return "ok"
    sender = msg.get("from", {}).get("first_name", "")
    if BOT_NAME in sender:
        return "ok"
    text = msg.get("text", "")
    ts = msg.get("date", "")
    chat = msg.get("chat", {}).get("title", "Telegram")
    requests.post(
        "https://api.mem.ai/v2/notes",
        headers={"Authorization": f"Bearer {MEM_KEY}"},
        json={"content": f"# MSG: {ts} | {text[:50]}\n\n__meta: last_writer=capturebot | last_written_at={ts}\n\n**Channel:** {chat}\n**Jatin:** {text}\n**MaxClaw:** [pending]", "collection_ids": [COLLECTION]}
    )
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
