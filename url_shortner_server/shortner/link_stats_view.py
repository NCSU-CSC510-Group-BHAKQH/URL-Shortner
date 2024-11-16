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

    def get(self, request: HttpRequest, special_code=None):
        """Handles GET requests to display link statistics or export CSV"""
        username = request.session.get("username", "")
        if not username:
            return redirect("signin")

        if request.path.endswith("/export-stats-csv/"):
            return self.export_stats_csv(request, special_code)

        # Get the link object by special_code and ensure it belongs to the current user
        link = get_object_or_404(Link, special_code=special_code, username=username)

        # Fetch all accesses for this link
        accesses = LinkAccess.objects.filter(link=link).order_by("-accessed_at")

        # Prepare context for the template
        context = {
            "link": link,
            "accesses": accesses,
        }

        return render(request, "homepages/linkstats.html", context=context)

    def export_stats_csv(self, request: HttpRequest, special_code):
        """Exports link statistics as CSV with date and time in filename"""
        username = request.session.get("username", "")
        if not username:
            return redirect("signin")

        # Get the link object by special_code and ensure it belongs to the current user
        link = get_object_or_404(Link, special_code=special_code, username=username)

        # Fetch all accesses for this link
        accesses = LinkAccess.objects.filter(link=link).order_by("-accessed_at")

        # Generate filename with current date and time
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"link_statistics_{current_datetime}.csv"

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(
            ["Access Time", "Device Type", "Browser", "City", "Region", "Country"]
        )

        for access in accesses:

            access_time = access.accessed_at if access else "Unknown"
            device_type = access.device_type if access else "Unknown"
            browser = access.browser if access else "Unknown"
            city = access.city if access else "Unknown"
            region = access.region if access else "Unknown"
            country = access.country if access else "Unknown"

            writer.writerow(
                [
                    access_time,
                    device_type,
                    browser,
                    city,
                    region,
                    country,
                ]
            )

        return response
