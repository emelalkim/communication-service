def send_email(recipient, content):
    # Simulate sending an email
    print(f"Sending email to {recipient}: {content}")
    return "Success"

def send_sms(recipient, content):
    # Simulate sending an SMS
    print(f"Sending SMS to {recipient}: {content}")
    return "Success"

def send_message(channel, recipient, content):
    if channel == "email":
        return send_email(recipient, content)
    elif channel == "sms":
        return send_sms(recipient, content)
    else:
        return "Channel not supported"
