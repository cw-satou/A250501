from flask import Flask, request, abort
from openai import OpenAI
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = 'O6C+OGyx9bHcMG5ltfz98NWzmA6zSjOwaL588inT2D0r0/EYBYxfR48dDTjAEDwQq5ZTa1zhHHhDQp5M9Wg1rdYjXFvK1xrJ/7UTwn46HKGXqaf8kKjO+fXBn0s6QC0VC/P/hsnlGFN4J4w0hfJRBwdB04t89/1O/w1cDnyilFU='

def reply_message(reply_token, text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }
    response = requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")

@app.route('/callback', methods=['POST'])
def callback():
    body = request.get_json()
    if body is None:
        abort(400)

    events = body.get('events', [])
    for event in events:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            client = OpenAI(api_key="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")

            response = client.responses.create(
                model="gpt-4.1",
                input="Write a one-sentence bedtime story about a unicorn."
            )

            reply_token = event['replyToken']
            reply_message(reply_token, response.output_text)

    return 'OK', 200

@app.route('/')
def index():
    return 'Flaskアプリは正常に動作しています'

if __name__ == '__main__':
    app.run(port=3000)
