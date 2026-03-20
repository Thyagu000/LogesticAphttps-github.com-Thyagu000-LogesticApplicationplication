from django.urls import path
from . import views

urlpatterns = [

    path('webhooks/', views.webhook_list, name="webhook_list"),

    path('webhooks/register/', views.register_webhook, name="register_webhook"),

    path('webhooks/delete/<int:id>/', views.delete_webhook, name="delete_webhook"),

]