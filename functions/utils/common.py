# -*- coding: utf-8 -*-
import os
import boto3

DYNAMO_DB_TABLE_NAME = os.environ.get('DYNAMO_DB_TABLE_NAME')
USER_POOL_ID = os.environ.get('USER_POOL_ID')
FROM_EMAIL = os.environ.get('FROM_EMAIL')

cog_client = boto3.client("cognito-idp")


def get_user_by_email(email):
    users = cog_client.list_users(
        UserPoolId=USER_POOL_ID,
        Filter=f'email="{email}"'
    )
    return users["Users"][0].get("Username") if users["Users"] else None
