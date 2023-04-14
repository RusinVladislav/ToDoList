from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture()
def category_create_data(faker) -> Callable:
    def _wrapper(*kwargs) -> dict:
        data = {'title': faker.sentence(1)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestCategoryCreateView:
    url = reverse('todolist.goals:create-category')

    def test_auth_required(self, client, category_create_data):
        """
        Неавторизованный пользователь при создании категории получит ошибку авторизации - 403
        """
        response = client.post(self.url, data={'title': category_create_data})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_board(self, auth_client, category_create_data):
        """
        Авторизованный пользователь не может создать удаленную категорию
        """

        response = auth_client.post(self.url, data=category_create_data(is_deleted=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['is_deleted'] is False
