"""The utils module defines many utility functions that don't fit into other specific modules."""

import re
from urllib.parse import urlparse
from typing import Tuple


def is_possibly_malicious(long_url: str) -> Tuple[bool, str | None]:
    """
    This function checks if a given URL is possibly malicious
    or contains phishing scams.

    It returns a tuple of with a boolean indicating the URL is
    in fact malicious, and a possible AnalysisID from VirusCheck.
    """
    malicious = False

    # 1. Check for HTTPS
    malicious = not long_url.startswith("https://")

    # 2. Check for suspicious patterns
    malicious = re.search(r"(login|verify|account|secure|bank)", long_url.lower())

    # 3. Check for IP address usage in the domain
    parsed_url = urlparse(long_url)
    malicious = re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed_url.netloc)

    # 4. Do VirusCheck
    virus_check_analysis_id = None

    # return (malicious, virus_check_analysis_id)
    return malicious
