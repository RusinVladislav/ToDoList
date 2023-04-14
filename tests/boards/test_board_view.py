import pytest

from django.urls import reverse
from rest_framework import status

from todolist.goals.models import BoardParticipant


@pytest.mark.django_db()
class TestBoardRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int):
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь при запросе доски получит ошибку авторизации
        """

        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_board(self, auth_client, board):
        """
        Авторизованный пользователь при запросе удаленной доски получит ошибку 404
        """

        board.is_deleted = True
        board.save()

        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_failed_to_retrieve_foregin_board(self, client, user_factory):
        """
        Авторизованный пользователь при запросе чужой доски получит ошибку 403
        """

        another_user = user_factory.create()
        client.force_login(another_user)

        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
class TestBoardRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int):
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь при удалении доски получит ошибку авторизации
        """

        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.reader,
    ], ids=['user role - writer', 'user role - reader'])
    def test_not_owner_failed_to_delete_board(self, client, user_factory, board, board_participant_factory, role):
        """
        Не владелец доски при ее удалении получит ошибку авторизации
        """

        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=role)
        client.force_login(another_user)

        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_to_delete_board(self, auth_client, board):
        """
        Владелец доски при ее удалении получит код 204 и в базе статус доски is_deleted станет True
        """

        response = auth_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        board.refresh_from_db()
        assert board.is_deleted is True

    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.reader,
        BoardParticipant.Role.owner,
    ], ids=['user role - writer', 'user role - reader'])
    def test_any_user_take_board(self, client, user_factory, board, board_participant_factory, role):
        """
        Любой пользователь может получить доску
        """

        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=role)
        client.force_login(another_user)

        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
