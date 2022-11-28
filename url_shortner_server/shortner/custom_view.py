"""new_view module defines the NewView view"""

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import View
import json

from shortner.models import Link


class CustomView(View):
    """CustomView is responsible for creation of custom shortened links"""

    def post(self, request: HttpRequest):
        """post handles post requests to /custom"""
        httpBody = json.loads(request.body)
        long_url = httpBody["long_url"]
        link = Link(long_url)
        custom_url = httpBody["custom_url"]
        link.save_custom(custom_url)
        response = link.to_json()
        return HttpResponse(response, status=201)
