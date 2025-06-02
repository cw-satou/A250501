from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # ここで受信データに応じた処理を行い、応答を返す
    return jsonify({'reply': 'メッセージを受け取りました！'})
