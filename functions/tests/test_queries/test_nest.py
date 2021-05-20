# -*- coding: utf-8 -*-
from functions.handler import main
from functions.utils.exceptions import UnauthorizedException

from functions.tests.base_tests import BaseTest


class TestNests(BaseTest):

    def setUp(self):
        super().setUp()
        self.event["info"]["parentTypeName"] = "Query"
        self.event["info"]["fieldName"] = "nest"
        self.event["arguments"]["nestId"] = "abc123"

    def test_get_nest_owner(self):
        self.assertTrue(main(self.event, {}))

    def test_get_nest_user(self):
        self.event["identity"]["username"] = "test_user1"
        self.assertTrue(main(self.event, {}))

    def test_get_nest_user_not_auth(self):
        self.event["identity"]["username"] = "test_user3"
        with self.assertRaises(UnauthorizedException):
            main(self.event, {})

    def test_get_nest_does_not_exist(self):
        self.event["arguments"]["nestId"] = "miata"
        with self.assertRaises(UnauthorizedException):
            main(self.event, {})
