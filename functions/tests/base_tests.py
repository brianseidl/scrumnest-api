# -*- coding: utf-8 -*-
from unittest import TestCase
import boto3
from moto import mock_dynamodb2  # mocking for dynamodb

from functions.utils.models import Nest, Story


@mock_dynamodb2
class BaseTest(TestCase):
    """
    Base Test class used to set up the Mock DynamoDB table used for unit testing
    """

    def setUp(self):
        """ Setup mock dynamodb table and base configuration"""

        # base event config
        self.event = {
            "identity": {
                "username": "test_admin"
            },
            "info": {},
            "arguments": {}
        }

        # dynamodb table
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.create_table(
            TableName='scrumnest-dev',
            KeySchema=[
                {
                    'AttributeName': 'nestId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'nestComponent',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'nestId',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'nestComponent',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        self.table.meta.client.get_waiter('table_exists').wait(TableName='scrumnest-dev')

        self.nest = Nest(
            'abc123',
            'NEST',
            name='Test Nest',
            owner='test_admin',
            users=[
                {
                    'username': 'test_user1',
                    'email': 'test_user1@gmail.com'
                },
                {
                    'username': 'test_user2',
                    'email': 'test_user2@gmail.com'
                }
            ]
        )
        self.nest.save()

        self.story1 = Story(
            'abc123',
            'STORY.123',
            title='test story 1',
            owner='test_admin'
        )
        self.story1.save()

    def tearDown(self):
        """
        Delete database resources and mock table
        """
        self.table.delete()
        self.dynamodb = None
