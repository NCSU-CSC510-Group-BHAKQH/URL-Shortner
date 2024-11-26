from unittest.mock import patch, MagicMock
from django.test import TestCase
from shortner.models import Link
from shortner.utils import do_security_check


class DoSecurityCheckTestCase(TestCase):
    def setUp(self):
        # Set up a sample link for testing
        self.link = Link.objects.create(
            long_url="https://example.com",
            username="testuser",
            possibly_malicious=False,
            vt_analysis_stats=None,
            vt_analysis_id=None,
        )

    @patch("shortner.utils.Client")
    def test_https_check_fails(self, mock_client):
        """Test that a non-HTTPS link is flagged as malicious."""
        self.link.long_url = "http://myetherevvalliet.com/"
        do_security_check(self.link)

        self.assertTrue(self.link.possibly_malicious)

    @patch("shortner.utils.Client")
    def test_suspicious_keyword_detection(self, mock_client):
        """Test that suspicious keywords in the URL are flagged as malicious."""
        self.link.long_url = "https://secure-login-example.com"
        do_security_check(self.link)

        self.assertTrue(self.link.possibly_malicious)

    @patch("shortner.utils.Client")
    def test_ip_address_in_domain(self, mock_client):
        """Test that a URL with an IP address in the domain is flagged as malicious."""
        self.link.long_url = "https://192.168.1.1"
        do_security_check(self.link)

        self.assertTrue(self.link.possibly_malicious)

    @patch("shortner.utils.Client")
    def test_virus_total_analysis_positive(self, mock_client):
        """Test that a link is flagged as malicious based on VirusTotal stats."""
        mock_analysis = MagicMock()
        mock_analysis.get.return_value = {"stats": {"malicious": 1, "suspicious": 0}}
        mock_client.return_value.scan_url.return_value = mock_analysis

        do_security_check(self.link)

        self.assertTrue(self.link.possibly_malicious)
        self.assertEqual(self.link.vt_analysis_stats, {"malicious": 1, "suspicious": 0})

    @patch("shortner.utils.Client")
    def test_virus_total_analysis_negative(self, mock_client):
        """Test that a link is not flagged as malicious if VirusTotal stats are clean."""
        mock_analysis = MagicMock()
        mock_analysis.get.return_value = {"stats": {"malicious": 0, "suspicious": 0}}
        mock_client.return_value.scan_url.return_value = mock_analysis

        do_security_check(self.link)

        self.assertFalse(self.link.possibly_malicious)
        self.assertEqual(self.link.vt_analysis_stats, {"malicious": 0, "suspicious": 0})

    # @patch("shortner.utils.Client")
    # def test_virus_total_api_error(self, mock_client):
    #     """Test that API errors in VirusTotal don't crash the function."""
    #     mock_client.side_effect = Exception("VirusTotal API error")

    #     do_security_check(self.link)

    #     self.assertFalse(self.link.possibly_malicious)  # Should remain unaffected

    def test_combined_checks(self):
        """Test that a combination of issues flags a URL as malicious."""
        self.link.long_url = "http://192.168.1.1/login"
        with patch("shortner.utils.Client") as mock_client:
            mock_analysis = MagicMock()
            mock_analysis.get.return_value = {"stats": {"malicious": 1, "suspicious": 0}}
            mock_client.return_value.scan_url.return_value = mock_analysis

            do_security_check(self.link)

        self.assertTrue(self.link.possibly_malicious)
