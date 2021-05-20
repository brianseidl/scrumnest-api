# -*- coding: utf-8 -*-
from functions.handler import main

from functions.tests.base_tests import BaseTest


class TestNests(BaseTest):

    def setUp(self):
        super().setUp()
        self.event["info"]["parentTypeName"] = "Query"
        self.event["info"]["fieldName"] = "nests"

    def test_get_nests_owner(self):
        actual = main(self.event, {})
        expected = 1  # list of length 1

        self.assertEqual(len(actual), expected)

    def test_get_nests_user(self):
        self.event["identity"]["username"] = "test_user1"

        actual = main(self.event, {})
        expected = 1  # list of length 1

        self.assertEqual(len(actual), expected)

    def test_get_nests_user_not_auth(self):
        self.event["identity"]["username"] = "test_user3"

        actual = main(self.event, {})
        expected = 0  # list of length 0

        self.assertEqual(len(actual), expected)
