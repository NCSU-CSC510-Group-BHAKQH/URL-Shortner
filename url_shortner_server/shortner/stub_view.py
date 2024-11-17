# pylint: disable=no-member
"""stub_view module has views for stub"""

from os import getenv

import requests
from django.http.response import HttpResponseRedirect
from django.views.generic import View

from user_agents import parse
from dotenv import load_dotenv

from shortner.constants import REDIRECT_404_URL
from shortner.models import Link, LinkAccess


class StubView(View):
    """StubView redirects user from stub to URL"""

    def get(self, _, stub: str):
        """get redirects user to the long url"""
        try:
            link = Link.objects.get(stub=stub)
            link.ctr += 1
            Link.objects.filter(username=link.username, stub=link.stub).update(
                ctr=link.ctr
            )

            user_agent_string = self.request.META.get("HTTP_USER_AGENT", "")
            user_agent = parse(user_agent_string)
            device_family = "PC" if user_agent.is_pc else user_agent.device.family

            #ip_address = self.request.META.get("REMOTE_ADDR", "")
            ip_address = "172.90.137.144"
            if ip_address == "127.0.0.1":
                city, region, country, latitude, longitude = (
                    "Localhost",
                    "Localhost",
                    "Localhost",
                    None,
                    None,
                )
            else:
                location = StubView.get_location(ip_address)
                city = location.get("city", "Unknown")
                region = location.get("region", "Unknown")
                country = location.get("country", "Unknown")
                loc = location.get("loc", None)
                latitude, longitude = (
                    map(float, loc.split(",")) if loc else (None, None)
                )
            print(latitude, longitude)
            LinkAccess.objects.create(
                link=link,
                ip_address=ip_address,
                user_agent=user_agent_string,
                browser=user_agent.browser.family,
                device_type=device_family,
                city=city,
                region=region,
                country=country,
                latitude=latitude,
                longitude=longitude,
            )

            return HttpResponseRedirect(link.long_url)
        except Link.DoesNotExist:  # pylint: disable=no-member
            return HttpResponseRedirect(REDIRECT_404_URL)

    @staticmethod
    def get_location(ip_address):
        """Gets the location of the user based on their IP address"""
        load_dotenv()
        token = getenv("IPINFO_API_TOKEN")
        url = f"https://ipinfo.io/{ip_address}/json?token={token}"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return {}
