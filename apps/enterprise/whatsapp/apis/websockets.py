import json

import requests
from django.http import JsonResponse
from django.views import View


class ReceiveMessageView(View):
    def post(self, request, *args, **kwargs):
        try:
            message = json.loads(request.body)
            print(message)
            url = "https://earnkraft.app.n8n.cloud/webhook-test/02069143-8c70-447a-aa05-02c797593676"
            requests.post(url, json=message, timeout=3)
            return JsonResponse({}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
