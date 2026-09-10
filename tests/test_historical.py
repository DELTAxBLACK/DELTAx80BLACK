"""
Tests for historical.py: ViewDNS must distinguish "source blocked or
unreachable" (None) from "source checked, genuinely no records" ([]).

Run from the project root:
    python3 -m unittest discover -s tests -v
or, if pytest is available:
    pytest tests/ -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from historical import fetch_viewdns_history


class TestFetchViewdnsHistory(unittest.TestCase):
    @patch("historical.requests.get")
    def test_403_returns_none_not_empty_list(self, mock_get):
        response = MagicMock()
        response.status_code = 403
        http_error = requests.exceptions.HTTPError(response=response)
        response.raise_for_status.side_effect = http_error
        mock_get.return_value = response

        result = fetch_viewdns_history("katabump.com", timeout=5)

        self.assertIsNone(result)  # None = "unavailable", never "no history"

    @patch("historical.requests.get")
    def test_other_http_error_also_returns_none(self, mock_get):
        response = MagicMock()
        response.status_code = 503
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=response
        )
        mock_get.return_value = response

        result = fetch_viewdns_history("katabump.com", timeout=5)

        self.assertIsNone(result)

    @patch("historical.requests.get")
    def test_timeout_returns_none(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("connect timeout")

        result = fetch_viewdns_history("katabump.com", timeout=5)

        self.assertIsNone(result)

    @patch("historical.requests.get")
    def test_connection_error_returns_none(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("refused")

        result = fetch_viewdns_history("katabump.com", timeout=5)

        self.assertIsNone(result)

    @patch("historical.requests.get")
    def test_success_with_no_table_returns_empty_list(self, mock_get):
        response = MagicMock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.text = "<html><body>nothing here</body></html>"
        mock_get.return_value = response

        result = fetch_viewdns_history("katabump.com", timeout=5)

        self.assertEqual(result, [])  # [] = genuinely checked, genuinely empty

    @patch("historical.requests.get")
    def test_success_with_records_parses_table(self, mock_get):
        response = MagicMock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.text = """
        <table border="1">
          <tr><th>IP</th><th>Location</th><th>Owner</th><th>Last Seen</th></tr>
          <tr><th>-</th><th>-</th><th>-</th><th>-</th></tr>
          <tr><td>203.0.113.5</td><td>US</td><td>Some Host</td><td>2024-01-01</td></tr>
        </table>
        """
        mock_get.return_value = response

        result = fetch_viewdns_history("katabump.com", timeout=5)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ip, "203.0.113.5")
        self.assertEqual(result[0].owner, "Some Host")
        self.assertEqual(result[0].last_seen, "2024-01-01")


if __name__ == "__main__":
    unittest.main()
