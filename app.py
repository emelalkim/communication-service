from flask import Flask, request, jsonify
from database import init_db, db
from models import MessageLog
from mock_send import send_message
from datetime import datetime, timedelta

app = Flask(__name__)
init_db(app)

@app.route("/sendMessage", methods=["POST"])
def send_message_endpoint():
    data = request.get_json()
    message_type = data.get("type")
    recipient = data.get("recipient")
    content = data.get("content")
    
    if not all([message_type, recipient, content]):
        return jsonify({"error": "Missing fields"}), 400

    status = send_message(message_type, recipient, content)

    message_log = MessageLog(type=message_type, recipient=recipient, content=content, status=status)
    db.session.add(message_log)
    db.session.commit()

    return jsonify({"status": status}), 200

@app.route("/messageLog", methods=["GET"])
def get_message_log():
    start_date_str = request.args.get("start")
    end_date_str = request.args.get("end")

    query = MessageLog.query
    if start_date_str:
        try:
            # Parse start date and set time to the beginning of the day
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            query = query.filter(MessageLog.timestamp >= start_date)
        except ValueError:
            return jsonify({"error": "Invalid start date format. Use YYYY-MM-DD"}), 400

    if end_date_str:
        try:
            # Parse end date and set time to the end of the day (23:59:59)
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
            query = query.filter(MessageLog.timestamp <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid end date format. Use YYYY-MM-DD"}), 400

    messages = query.all()
    result = [
        {
            "id": message.id,
            "type": message.type,
            "recipient": message.recipient,
            "content": message.content,
            "status": message.status,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for message in messages
    ]

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)