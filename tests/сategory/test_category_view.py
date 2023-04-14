import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestCategoryRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(category_pk: int):
        return reverse('todolist.goals:category', kwargs={'pk': category_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь при запросе категории получит ошибку авторизации
        """

        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_category(self, auth_client, category):
        """
        Авторизованный пользователь при запросе удаленной категории получит ошибку 404
        """

        category.is_deleted = True
        category.save()

        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
class TestBoardRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.category_id)

    @staticmethod
    def get_url(category_pk: int):
        return reverse('todolist.goals:category', kwargs={'pk': category_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь при удалении категории получит ошибку авторизации
        """

        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN