"""stub_view module has views for stub"""

from django.http.response import HttpResponseRedirect
from django.views.generic import View

from shortner.constants import REDIRECT_404_URL
from shortner.models import Link, LinkAccess

from user_agents import parse


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

            user_agent_string = self.request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)

            LinkAccess.objects.create(
                link=link,
                ip_address=self.request.META.get('REMOTE_ADDR', ''),
                user_agent=user_agent_string,
                browser=user_agent.browser.family,
                device_type=user_agent.device.family,
            )

            return HttpResponseRedirect(link.long_url)
        except Link.DoesNotExist:  # pylint: disable=no-member
            return HttpResponseRedirect(REDIRECT_404_URL)
