"""stub_view module has views for stub"""

import os

import requests
from django.http.response import HttpResponseRedirect
from django.views.generic import View

from shortner.constants import REDIRECT_404_URL
from shortner.models import Link, LinkAccess

from user_agents import parse
from dotenv import load_dotenv
from os import getenv


class StubView(View):
    """StubView redirects user from stub to URL"""

    def get(self, _, stub: str):
        """get redirects user to the long url"""
        try:
            link = Link.objects.get(stub=stub)  # pylint: disable=no-member
            link.ctr += 1
            Link.objects.filter(
                username=link.username, stub=link.stub  # pylint: disable=no-member
            ).update(ctr=link.ctr)

            user_agent_string = self.request.META.get("HTTP_USER_AGENT", "")
            user_agent = parse(user_agent_string)
            device_family = "PC" if user_agent.is_pc else user_agent.device.family

            ip_address = self.request.META.get("REMOTE_ADDR", "")
            # ip_address = "71.69.163.169"
            if ip_address == "127.0.0.1":
                city, region, country = "Localhost", "Localhost", "Localhost"
            else:
                location = StubView.get_location(ip_address)
                city = location.get("city", "Unknown")
                region = location.get("region", "Unknown")
                country = location.get("country", "Unknown")

            LinkAccess.objects.create(
                link=link,
                ip_address=ip_address,
                user_agent=user_agent_string,
                browser=user_agent.browser.family,
                device_type=device_family,
                city=city,
                region=region,
                country=country,
            )

            return HttpResponseRedirect(link.long_url)
        except Link.DoesNotExist:  # pylint: disable=no-member
            return HttpResponseRedirect(REDIRECT_404_URL)

    def get_location(ip_address):
        load_dotenv()
        token = os.getenv("IPINFO_API_TOKEN")
        url = f"https://ipinfo.io/{ip_address}/json?token={token}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return {}
