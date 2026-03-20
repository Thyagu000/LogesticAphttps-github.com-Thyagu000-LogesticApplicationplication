from django.urls import path
from .views import (
    NotificationListView,
    NotificationCreateView,
    MarkNotificationReadView
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("create/", NotificationCreateView.as_view(), name="notification-create"),
    path("<uuid:pk>/read/", MarkNotificationReadView.as_view(), name="notification-read"),
]