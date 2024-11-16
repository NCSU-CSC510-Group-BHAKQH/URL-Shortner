# pylint: disable=no-member
"""delete_view module defines the view that user wants to delete"""
import json

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect

from shortner.models import Link


class DeleteView(View):
    """DeleteView is responsible for deletion of the shortened links"""

    def get(
        self, request: HttpRequest, special_code: str
    ):  # pylint: disable=unused-argument
        """delete handles requests to be deleted /delete"""
        special_codes = special_code
        try:
            member = Link.objects.get(
                special_code=special_codes
            )  # pylint: disable=no-member
            member.delete()
            return redirect("list")
        except Exception as e:  # pylint: disable=broad-exception-caught
            error_msg = {"exception": str(e)}
            return HttpResponse(json.dumps(error_msg), status=404)
