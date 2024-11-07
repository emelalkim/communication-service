from abc import ABC, abstractmethod

class MessageSender(ABC):
    @abstractmethod
    def send_message(self, recipient: str, content: str) -> str:
        """Send a message to the recipient with the specified content."""
        pass

class SMSSender(MessageSender):
    def send_message(self, recipient: str, content: str) -> str:
        # Mock sending an SMS message
        print(f"Sending SMS to {recipient}: {content}")
        return "Success"

class EmailSender(MessageSender):
    def send_message(self, recipient: str, content: str) -> str:
        # Mock sending an email message
        print(f"Sending Email to {recipient}: {content}")
        return "Success"

def get_sender(channel: str) -> MessageSender:
    """Return the appropriate message sender based on the channel type."""
    if channel.lower() == "sms":
        return SMSSender()
    elif channel.lower() == "email":
        return EmailSender()
    else:
        raise ValueError("Channel not supported")

def send_message(channel: str, recipient: str, content: str) -> str:
    """
    Coordinator function to send a message.
    
    Args:
        channel (str): The message channel, e.g., "sms" or "email".
        recipient (str): The recipient's contact information.
        content (str): The content of the message.
    
    Returns:
        str: The status of the message sending operation.
    """
    try:
        sender = get_sender(channel)  # Get the appropriate sender based on the channel
        status = sender.send_message(recipient, content)
        return status
    except ValueError as e:
        # Handle unsupported message channel
        print(f"Error: {e}")
        return "Channel not supported"
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred while sending the message."