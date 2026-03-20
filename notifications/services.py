from .models import Notification
from .email_service import send_notification_email
from .sms_service import send_notification_sms


def create_notification(user, notification_type, reference_id=None):
    """
    Reusable function to create notifications + send email + send SMS
    """

    # Auto title + message based on type
    if notification_type == Notification.NotificationType.SHIPMENT_ASSIGNED:
        title = "Shipment Assigned"
        message = "A shipment has been assigned to you."

    elif notification_type == Notification.NotificationType.DELIVERY_UPDATE:
        title = "Delivery Status Updated"
        message = "Your shipment delivery status has been updated."

    elif notification_type == Notification.NotificationType.PAYMENT_RECEIVED:
        title = "Payment Received"
        message = "Payment has been successfully received."

    elif notification_type == Notification.NotificationType.PAYOUT_PROCESSED:
        title = "Payout Processed"
        message = "Your payout has been processed."

    else:
        return None

    # Create notification in DB
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=notification_type,
        reference_id=reference_id
    )

    # Send Email
    send_notification_email(user, title, message)

    # Send SMS (mock)
    send_notification_sms(user, message)

    return notification