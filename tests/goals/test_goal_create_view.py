from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture()
def goal_create_data(faker) -> Callable:
    def _wrapper(*kwargs) -> dict:
        data = {
            'title': faker.sentence(2),
            'description': faker.sentence(10),
            'category': 1,
        }
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestGoalCreateView:
    url = reverse('todolist.goals:create-goal')

    def test_auth_required(self, client, goal_create_data):
        """
        Неавторизованный пользователь при создании цели получит ошибку авторизации - 403
        """
        response = client.post(self.url, data=goal_create_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_goal(self, auth_client, goal_create_data):
        """
        Авторизованный пользователь не может создать удаленную цель
        """

        response = auth_client.post(self.url, data=goal_create_data(is_deleted=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['is_deleted'] is False
