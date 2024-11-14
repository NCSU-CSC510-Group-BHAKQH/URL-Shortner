import csv
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.views.generic import View
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from datetime import datetime
from shortner.models import Link, LinkAccess


class LinkStatsView(View):
    """StatsView is responsible for displaying and exporting link statistics"""

    def get(self, request, special_code):
        """Handles GET requests to display link statistics or export CSV"""
        username = request.session.get("username", "")
        if not username:
            return redirect("signin")

        # Get the link object by special_code and ensure it belongs to the current user
        link = get_object_or_404(Link, special_code=special_code, username=username)
        print(link.long_url)

        # Fetch all accesses for this link
        accesses = LinkAccess.objects.filter(link=link).order_by('-accessed_at')

        # Prepare context for the template
        context = {
            "link": link,
            "accesses": accesses,
        }

        return render(request, "homepages/linkstats.html", context=context)

