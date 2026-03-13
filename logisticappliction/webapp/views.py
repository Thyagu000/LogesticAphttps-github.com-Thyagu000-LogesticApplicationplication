from django.shortcuts import render

# Create your views here.
import requests
import time
from django.shortcuts import render, redirect
from .models import Webhook, WebhookLog


# CREATE - Register Webhook
def register_webhook(request):

    if request.method == "POST":

        webhook_url = request.POST.get("webhook_url")
        event = request.POST.get("event")

        Webhook.objects.create(
            webhook_url=webhook_url,
            event=event
        )

        return redirect('webhook_list')

    return render(request, "webhooks/register.html")


# READ - List Webhooks
def webhook_list(request):

    webhooks = Webhook.objects.all()

    return render(request, "webhooks/list.html", {"webhooks": webhooks})


# DELETE Webhook
def delete_webhook(request, id):

    webhook = Webhook.objects.get(id=id)
    webhook.delete()

    return redirect("webhook_list")


# Trigger Webhook Event
def trigger_webhook(event_name, data):

    webhooks = Webhook.objects.filter(event=event_name)

    for webhook in webhooks:

        retry = 3

        for attempt in range(retry):

            try:

                response = requests.post(webhook.webhook_url, json=data)

                if response.status_code == 200:

                    WebhookLog.objects.create(
                        webhook=webhook,
                        status="SUCCESS",
                        response=response.text
                    )

                    break

            except Exception as e:

                if attempt == retry - 1:

                    WebhookLog.objects.create(
                        webhook=webhook,
                        status="FAILED",
                        response=str(e)
                    )

                time.sleep(2)