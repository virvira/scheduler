from typing import Type

import pytest
from rest_framework.test import APIClient

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> Type[APIClient]:
    return APIClient


def auth_client(client, user) -> Type[APIClient]:
    client.force_login(user)
    return client
