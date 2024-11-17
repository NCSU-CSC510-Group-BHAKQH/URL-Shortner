# pylint: disable=no-member
"""Django view for the link statistics page."""
from django.http.request import HttpRequest
from django.views.generic import View
from django.shortcuts import redirect, render
from shortner.models import Link, LinkAccess


class USMapView(View):
    """StatsView is responsible for displaying and exporting link statistics"""

    def get(self, request: HttpRequest, link_stub: str = None):
        """Handles GET requests to display link statistics or export CSV"""
        username = request.session.get("username", "")
        if not username:
            return redirect("signin")


        if link_stub:
            link = Link.objects.get(special_code=link_stub, username=username)
            link_accesses = LinkAccess.objects.filter(link=link)
        else:
            # If no link_stub is provided, fetch all LinkAccess for the user's links
            links = Link.objects.filter(username=username)
            link_accesses = LinkAccess.objects.filter(link__in=links)

        access_data = [
            {
                "city": access.city,
                "region": access.region,
                "latitude": access.latitude,
                "longitude": access.longitude,
            }
            for access in link_accesses
        ]
        context = {"access_data": access_data}

        return render(request, "homepages/us_map.html", context=context)