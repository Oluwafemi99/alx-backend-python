#!/usr/bin/env python3
"""Unit tests for utility functions: access_nested_map, get_json,
and memoize to test that all utility functions are working as
espected                                                       """

import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import patch, Mock


# test for aceess_nested_map
class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map utility function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected value for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

# test for keyerror
    @parameterized.expand([
        ({}, ('a')),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json utility function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected payload and calls requests.get with
            correct URL."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Calling the function
        result = get_json(test_url)

        # assertion
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize utility function."""
    def test_memoize(self):
        """
        Test that the memoize decorator caches the result of a method.
        This ensures that a_method is only called once even if the
        memoized property is accessed multiple times.
        """

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:

            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            # test the memoize
        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)

        # making sure the test is ran once
        mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
