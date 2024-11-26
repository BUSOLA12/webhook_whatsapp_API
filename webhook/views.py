from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

VERIFY_TOKEN = "EAARMPZAdjRHEBOycdcSP1oKH2uuZAM0RZBpQZAfxfBtUIFb2VpTmsa3UlEg3IQWmMRJKZCxeuHIGA9OMCU3QGdnNRYbWayByiQ7JjZCkPZAiZA2WY8eWNhJS8srCWMS0xHSI8NLyK04RFLbZCqhCYhOebJAcdijHr4MOfqL5bmAVZBYOrASZAF6S62LOKaObcwdBiNJ2ryapgpPAfJCAfnQoccZBxbsfPf8ZD"  # Replace with your own token

# Webhook Verification
def webhook_verify(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse("Forbidden", status=403)

# Handle Incoming Messages
@csrf_exempt
def webhook_handler(request):
    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))
        print("Webhook Data:", payload)

        # Check if it's a message event
        if payload.get("object") == "whatsapp_business_account":
            for entry in payload.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        # Extract message details
                        message = value["messages"][0]
                        from_number = message["from"]  # Sender's number
                        message_body = message.get("text", {}).get("body", "")  # Text content

                        print(f"Message from {from_number}: {message_body}")

        return JsonResponse({"status": "success"}, status=200)

    return HttpResponse("Invalid request", status=400)

