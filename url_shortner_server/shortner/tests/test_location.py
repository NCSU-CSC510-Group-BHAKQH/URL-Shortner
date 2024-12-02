import unittest
from unittest.mock import patch, MagicMock
from shortner.stub_view import StubView


class TestGetLocation(unittest.TestCase):
    def setUp(self):
        self.valid_ip = "8.8.8.8"
        self.invalid_ip = "999.999.999.999"
        self.mock_token = "mock_api_token"

    @patch("shortner.views.stub_view.getenv")
    @patch("shortner.views.stub_view.requests.get")
    def test_valid_ip_address(self, mock_get, mock_getenv):
        """Test with a valid IP address and a successful API response."""
        # Mock environment variable for API token
        mock_getenv.return_value = self.mock_token

        # Mock response for a valid IP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "city": "Mountain View",
            "region": "California",
            "country": "US",
            "loc": "37.3861,-122.0839",
        }
        mock_get.return_value = mock_response

        # Call the function
        result = StubView.get_location(self.valid_ip)

        # Assertions
        self.assertEqual(result["city"], "Mountain View")
        self.assertEqual(result["region"], "California")
        self.assertEqual(result["country"], "US")
        self.assertEqual(result["loc"], "37.3861,-122.0839")
        mock_get.assert_called_once_with(
            f"https://ipinfo.io/{self.valid_ip}/json?token={self.mock_token}", timeout=30
        )

    @patch("shortner.views.stub_view.getenv")
    @patch("shortner.views.stub_view.requests.get")
    def test_invalid_ip_address(self, mock_get, mock_getenv):
        """Test with an invalid IP address resulting in a non-200 response."""
        # Mock environment variable for API token
        mock_getenv.return_value = self.mock_token

        # Mock response for an invalid IP
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        # Call the function
        result = StubView.get_location(self.invalid_ip)

        # Assertions
        self.assertEqual(result, {})
        mock_get.assert_called_once_with(
            f"https://ipinfo.io/{self.invalid_ip}/json?token={self.mock_token}", timeout=30
        )

    @patch("shortner.views.stub_view.getenv")
    @patch("shortner.views.stub_view.requests.get")
    def test_request_timeout(self, mock_get, mock_getenv):
        """Test that the function handles request timeouts gracefully."""
        # Mock environment variable for API token
        mock_getenv.return_value = self.mock_token

        # Simulate a timeout exception
        mock_get.side_effect = requests.Timeout

        # Call the function
        result = StubView.get_location(self.valid_ip)

        # Assertions
        self.assertEqual(result, {})
        mock_get.assert_called_once_with(
            f"https://ipinfo.io/{self.valid_ip}/json?token={self.mock_token}", timeout=30
        )

    @patch("shortner.views.stub_view.getenv")
    @patch("shortner.views.stub_view.requests.get")
    def test_network_error(self, mock_get, mock_getenv):
        """Test that the function handles network errors gracefully."""
        # Mock environment variable for API token
        mock_getenv.return_value = self.mock_token

        # Simulate a general network exception
        mock_get.side_effect = requests.RequestException

        # Call the function
        result = StubView.get_location(self.valid_ip)

        # Assertions
        self.assertEqual(result, {})
        mock_get.assert_called_once_with(
            f"https://ipinfo.io/{self.valid_ip}/json?token={self.mock_token}", timeout=30
        )


if __name__ == "__main__":
    unittest.main()
