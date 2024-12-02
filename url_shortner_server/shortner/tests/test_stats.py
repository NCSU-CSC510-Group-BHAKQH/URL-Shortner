import pytest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from shortner.models import Link
from datetime import datetime


class TestViews(TestCase):
    """Views test class"""

    def setUp(self):
        """Set up necessary data for tests"""
        # Define user credentials and info
        self.username = "testuser123"
        self.password = "password123"
        self.fname = "John"
        self.lname = "Doe"
        self.email = "john.doe@example.com"

        # Create the user
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name=self.fname,
                                             last_name=self.lname, email=self.email)

        # Define link and related objects
        self.link = Link.objects.create(username=self.username, long_url="http://example.com")

        # Define URLs for easy use
        self.add_new_url = reverse("add_new")
        self.update_url = reverse("update")
        self.stats_url = reverse("stats")

    def tearDown(self):
        """Clean up any data after tests"""
        User.objects.all().delete()
        Link.objects.all().delete()

    def test_stats_view_authenticated(self):
        """Test stats view when authenticated"""
        # Log in the user
        self.client.post(reverse('signin'), {'username': self.username, 'pass1': self.password, 'fname': self.fname})

        # Access the stats page
        response = self.client.get(self.stats_url)

        # Assert the status and template used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepages/urlstats.html")

    def test_stats_view_unauthenticated(self):
        """Test stats view when not authenticated"""
        response = self.client.get(self.stats_url)
        self.assertRedirects(response, reverse('signin'))

    def test_export_csv_authenticated(self):
        """Test export CSV functionality when authenticated"""
        # Log in the user
        self.client.post(reverse('signin'), {'username': self.username, 'pass1': self.password, 'fname': self.fname})

        # Add a link
        self.client.post(self.add_new_url, {"long-url": "https://www.example.com"})

        # Access export CSV
        response = self.client.get(reverse("export_csv"))

        # Assert correct status and content type for CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertTrue(response["Content-Disposition"].startswith('attachment; filename="all_url_statistics_'))

    def test_export_csv_unauthenticated(self):
        """Test export CSV when not authenticated"""
        response = self.client.get(reverse("export_csv"))
        self.assertRedirects(response, reverse('signin'))

    def test_export_csv_content(self):
        """Test the content of the exported CSV"""
        # Log in and add a link
        self.client.post(reverse('signin'), {'username': self.username, 'pass1': self.password, 'fname': self.fname})
        self.client.post(self.add_new_url, {"long-url": "https://www.example.com"})

        # Access and parse the CSV response
        response = self.client.get(reverse("export_csv"))
        content = response.content.decode("utf-8")
        self.assertIn("Long URL", content)  # Verify column headers
        self.assertIn("https://www.example.com", content)  # Verify the link
