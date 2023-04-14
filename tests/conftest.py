import pytest
from rest_framework.test import APIClient

pytest_plugins = 'tests.factories'

@pytest_fixture()
def client() -> APIClient:
    return APIClient()

@pytest_fixture()
def auth_client(client, user) -> APIClient:
    client.force_login(user)
    return client
