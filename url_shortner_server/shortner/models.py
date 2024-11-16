"""Models module deals with models representing entities in the application"""

import json
from random import seed, choice
from uuid import uuid4

from django.db import models

from shortner.constants import CHARS, STUB_LENGTH


class Link(models.Model):
    """Link model refers to a conversion of a long URL to a shortened one"""

    # 2083 is the max length of URL supported by Microsoft Edge
    long_url = models.CharField(max_length=2083)
    special_code = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    stub = models.CharField(max_length=STUB_LENGTH, unique=True)
    username = models.CharField(max_length=2083, default="xxx")
    ctr = models.IntegerField(blank=True, null=True)
    possibly_malicious = models.BooleanField(default=False)
    vt_analysis_id = models.CharField(max_length=128, null=True)
    vt_analysis_stats = models.JSONField(null=True)

    def save(self, *args, **kwargs):
        seed(str(self.special_code))
        self.stub = "".join(choice(CHARS) for _ in range(STUB_LENGTH))
        self.ctr = 0
        super().save(*args, **kwargs)

    def save_custom(self, custom_stub, *args, **kwargs):
        """check if the custom_stub is already in use by the user"""
        self.stub = custom_stub
        self.ctr = 0
        super().save(*args, **kwargs)

    def to_json(self):
        """to_json converts link to JSON string"""
        return json.dumps(
            {
                "long_url": self.long_url,
                "special_code": str(self.special_code),
                "stub": self.stub,
            }
        )


class LinkAccess(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="accesses")
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=512)
    browser = models.CharField(max_length=64)
    device_type = models.CharField(max_length=64)
    accessed_at = models.DateTimeField(auto_now_add=True)

    city = models.CharField(max_length=128, default="Unknown")
    region = models.CharField(max_length=128, default="Unknown")
    country = models.CharField(max_length=128, default="Unknown")

    def __str__(self):
        return f"Accessed {self.link} on {self.accessed_at}"


def give_link_by_username_long_url(username, long_url):
    """filter by username and long url"""
    link = Link.objects.get(
        username=username, long_url=long_url
    )  # pylint: disable=no-member
    return link


def give_links(username):
    """filter by username"""
    links = Link.objects.filter(username=username)  # pylint: disable=no-member
    return links
