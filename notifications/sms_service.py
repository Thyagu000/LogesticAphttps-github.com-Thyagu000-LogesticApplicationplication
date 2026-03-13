def send_notification_sms(user, message):
    """
    Mock SMS sending service.
    In production, integrate with SMS gateway (Twilio, MSG91, etc.)
    """

    # Assuming user has phone number field in future
    # For now we simulate SMS sending

    print("📱 SMS SENT")
    print(f"To User: {user.username}")
    print(f"Message: {message}")
    print("--------------------------------------------------")

    return True