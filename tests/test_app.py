import json
from models import MessageLog
from database import db
from datetime import datetime, timedelta, timezone

def test_send_message_success(client):
    # Prepare test data
    data = {
        "type": "email",
        "recipient": "test@example.com",
        "content": "Hello, this is a test message."
    }
    
    # Send a POST request to /sendMessage
    response = client.post("/sendMessage", data=json.dumps(data), content_type="application/json")
    
    # Assert that the response status code is 200 and status is 'Success'
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["status"] == "Success"

    # Check that the message was logged in the database
    message_log = MessageLog.query.first()
    assert message_log is not None
    assert message_log.type == data["type"]
    assert message_log.recipient == data["recipient"]
    assert message_log.content == data["content"]
    assert message_log.status == "Success"

def test_send_message_missing_fields(client):
    # Prepare incomplete test data
    data = {
        "type": "email",
        "content": "Missing recipient."
    }
    
    # Send a POST request to /sendMessage
    response = client.post("/sendMessage", data=json.dumps(data), content_type="application/json")
    
    # Assert that the response status code is 400 due to missing fields
    assert response.status_code == 400
    response_data = response.get_json()
    assert "error" in response_data
    assert response_data["error"] == "Missing fields"

def test_send_message_unsupported_channel(client):
    # Prepare test data with an unsupported channel type
    data = {
        "type": "unsupported_channel",
        "recipient": "test@example.com",
        "content": "This channel is not supported."
    }
    
    # Send a POST request to /sendMessage
    response = client.post("/sendMessage", data=json.dumps(data), content_type="application/json")
    
    # Assert that the response status code is 200 and status is 'Channel not supported'
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["status"] == "Channel not supported"

    # Verify the log entry in the database
    message_log = MessageLog.query.first()
    assert message_log is not None
    assert message_log.status == "Channel not supported"

def test_message_log_no_filter(client):
    # Add sample messages to the database
    message1 = MessageLog(type="email", recipient="user1@example.com", content="Message 1", status="Success")
    message2 = MessageLog(type="sms", recipient="1234567890", content="Message 2", status="Success")
    db.session.add_all([message1, message2])
    db.session.commit()

    # Send GET request without filters
    response = client.get("/messageLog")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_message_log_with_date_filter(client):
    # Add sample messages with specific timestamps
    now = datetime.now(timezone.utc)
    message1 = MessageLog(type="email", recipient="user1@example.com", content="Message 1", status="Success", timestamp=now - timedelta(days=2))
    message2 = MessageLog(type="sms", recipient="1234567890", content="Message 2", status="Success", timestamp=now - timedelta(days=1, hours=1))  # Slightly before 'today'
    message3 = MessageLog(type="sms", recipient="1234567890", content="Message 3", status="Success", timestamp=now)
    db.session.add_all([message1, message2, message3])
    db.session.commit()

    # Define start and end dates for filtering to cover full days
    start_date = (now - timedelta(days=3)).strftime("%Y-%m-%d")  # Includes full day
    end_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")  # Includes up to 'now'

    # Send GET request with date range filter
    response = client.get(f"/messageLog?start={start_date}&end={end_date}")
    assert response.status_code == 200
    data = response.get_json()
    
    # Expect messages within the last 3 days, including all 3 added messages
    assert len(data) == 2  # Should return message1, message2, and message3

def test_message_log_invalid_date_format(client):
    # Attempt to filter with an invalid date format
    response = client.get("/messageLog?start=2024-13-01")  # Invalid month
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid start date format. Use YYYY-MM-DD"
