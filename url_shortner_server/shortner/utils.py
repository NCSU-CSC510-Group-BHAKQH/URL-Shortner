"""The utils module defines many utility functions that don't fit into other specific modules."""

from os import getenv
import re
from urllib.parse import urlparse

from dotenv import load_dotenv
from vt import Client
from vt.error import APIError

from shortner.models import Link


def do_security_check(link: Link) -> None:
    """
    This function checks if a given Link is possibly malicious
    or contains phishing scams.
    """
    load_dotenv()
    malicious = False

    long_url = link.long_url

    # 1. Check for HTTPS
    if not long_url.startswith("https://"):
        malicious = True

    # 2. Check for suspicious patterns
    if re.search(r"(login|verify|account|secure|bank)", long_url.lower()):
        malicious = True

    # 3. Check for IP address usage in the domain
    parsed_url = urlparse(long_url)
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed_url.netloc):
        malicious = True

    # 4. Do VirusCheck
    with Client(getenv("VIRUSTOTAL_API_KEY")) as vt_client:
        try:
            analysis = vt_client.scan_url(long_url, True)
            if analysis:
                a_stats = dict(analysis.get("stats"))
                if a_stats["malicious"] > 0 or a_stats["suspicious"] > 0:
                    link.vt_analysis_stats = a_stats
                    link.vt_analysis_id = analysis.id
                    malicious = True
        except APIError:
            pass

    link.possibly_malicious = malicious
