from django.core.mail import send_mail
from django.conf import settings


def send_notification_email(user, subject, message):
    """
    Sends email notification to user
    """

    if not user.email:
        return False  # No email available

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return True