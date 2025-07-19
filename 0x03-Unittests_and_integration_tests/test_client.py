#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class from client.py.

This module tests that:
- The `org` method correctly returns GitHub organization information.
- External HTTP calls are mocked using `unittest.mock.patch`.
- The test is parameterized to test multiple organization names.
"""
import unittest
from unittest.mock import patch
from client import GithubOrgClient
from parameterized import parameterized


"""
    Test suite for the GithubOrgClient class.

    This class focuses on testing the `.org` method to ensure it returns
    the expected result from the GitHub API and does not make actual HTTP
    requests.
    """


class TestGithubOrgClient(unittest.TestCase):
    """
        Test that GithubOrgClient.org returns the expected organization
        payload.

        Args:
            org_name (str): The name of the GitHub organization to test.
            expected_result (dict): The mock JSON payload to return.
            mock_get_json (Mock): The mocked version of get_json to avoid HTTP
            calls.

        Steps:
        1. Patch the `get_json` method so that it returns `expected_result`.
        2. Initialize the `GithubOrgClient` with the test `org_name`.
        3. Access the `.org` property to trigger the patched method.
        4. Assert that the returned result matches `expected_result`.
        5. Assert that `get_json` was called exactly once with the correct URL.

        The test uses memoization, so it should only call `get_json` once.
        """

    @parameterized.expand([
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_result, mock_get_json):

        # Set the return value of the mocked get_json
        mock_get_json.return_value = expected_result

        # Create the client and access the org property
        client = GithubOrgClient(org_name)
        result = client.org

        # perform the test and Json shold be called properly
        self.assertEqual(result, expected_result)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")


if __name__ == '__main__':
    unittest.main()
