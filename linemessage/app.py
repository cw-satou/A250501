from flask import Flask, request, abort
from openai import OpenAI
import requests
import os

app = Flask(__name__)

def reply_message(reply_token, text):
    CHANNEL_ACCESS_TOKEN=os.getenv("CHANNEL_ACCESS_TOKEN")
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
    response = requests.post(
        'https://api.line.me/v2/bot/message/reply', headers=headers, json=data)
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
            api_key = os.getenv("OPENAI_API_KEY")

            # プロジェクトAPIキーをここに記入
            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4o",  # 利用したいモデル名
                messages=[
                    {"role": "system", "content": "あなたは役立つアシスタントです。"},
                    {"role": "user", "content": "日本の四季について教えてください。"}
                ]
            )

            reply_token = event['replyToken']
            reply_message(reply_token, response.choices[0].message.content)

    return 'OK', 200


@app.route('/')
def index():
    return 'Flaskアプリは正常に動作しています'


if __name__ == '__main__':
    app.run(port=3000)
