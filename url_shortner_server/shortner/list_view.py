# pylint: disable=no-member
"""Django view for listing the URLs."""
from django.http.request import HttpRequest
from django.views.generic import View
from django.shortcuts import redirect, render

from shortner.models import Link


class ListUrlsView(View):
    """NewView is responsible for creation of new shortened links"""

    def get(self, request: HttpRequest):
        """post handles post requests to /new"""
        username = request.session["username"]
        context = {}
        if username == "":
            redirect("signin")
        list_of_links = Link.objects.filter(
            username=username
        )  # pylint: disable=no-member
        context["list_of_links"] = []
        for link_obj in list_of_links:
            x = {}
            x["long_url"] = link_obj.long_url
            x["short_url"] = request.build_absolute_uri("/") + "stub/" + link_obj.stub
            x["special_code"] = link_obj.special_code
            x["possibly_malicious"] = link_obj.possibly_malicious
            x["vt_analysis_id"] = link_obj.vt_analysis_id
            context["list_of_links"].append(x)

        return render(request, "homepages/listurls.html", context=context)
