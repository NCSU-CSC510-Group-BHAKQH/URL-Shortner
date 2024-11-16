# pylint: disable=no-member
"""
vt_stats_view.py
~~~~~~~~~~~~~~~~
Django view for viewing VirusTotal stats.
"""

from django.http.request import HttpRequest
from django.views.generic import View
from django.shortcuts import redirect, render

from shortner.models import Link


class VirusTotalStatsView(View):
    """Shows the VirusTotal stats for a given link."""

    def get(self, request: HttpRequest):
        """Gets the VT stats view page."""
        username = request.session.get("username", "")
        long_url = request.GET.get("long_url")

        if username == "":
            redirect("signin")

        link = Link.objects.get(username=username, long_url=long_url)

        stats = link.vt_analysis_stats

        context = {
            "long_url": long_url,
            "malicious": stats["malicious"],
            "suspicious": stats["suspicious"],
            "undetected": stats["undetected"],
            "harmless": stats["harmless"],
            "timeout": stats["timeout"],
        }

        return render(request, "other/vt_stats.html", context=context)
