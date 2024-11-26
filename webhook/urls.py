from django.urls import path
from .views import webhook_verify, webhook_handler

urlpatterns = [
    path("webhook/", webhook_verify, name="webhook_verify"),
    path("webhook", webhook_handler, name="webhook_handler"),  # WhatsApp may send without trailing slash
]
