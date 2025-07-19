#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class from client.py.

This module tests that:
- The `org` method correctly returns GitHub organization information.
- External HTTP calls are mocked using `unittest.mock.patch`.
- The test is parameterized to test multiple organization names.
"""
import unittest
from unittest.mock import patch, PropertyMock
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
        
    def test_public_repos_url(self):
        """ Test that _public_repos_url returns the correct repos_url.
        Steps:
        1. Patch the `.org` property to return a predefined dictionary.
        2. Access the `_public_repos_url` property.
        3. Assert that it returns the expected URL from the mock.
        """
        # Define the mocked payload
        mock_payload = {"repos_url":
                        "https://api.github.com/orgs/testorg/repos"}

        # Use patch.object as a context manager to mock the `.org` property
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock
                          ) as mock_org:
            mock_org.return_value = mock_payload  # Mocked return value

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, mock_payload["repos_url"])


if __name__ == '__main__':
    unittest.main()
