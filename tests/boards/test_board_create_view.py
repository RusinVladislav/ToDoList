from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status

from todolist.goals.models import BoardParticipant


@pytest.fixture()
def board_create_data(faker) -> Callable:
    def _wrapper(*kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestBoardCreateView:
    url = reverse('todolist.goals:create_board')

    def test_auth_required(self, client, board_create_data):
        """
        Неавторизованный пользователь при создании доски получит ошибку авторизации - 403
        """
        response = client.post(self.url, data={'title': board_create_data})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_board(self, auth_client, board_create_data):
        """
        Авторизованный пользователь не может создать удаленную доску
        """

        response = auth_client.post(self.url, data=board_create_data(is_deleted=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['is_deleted'] is False

    def test_request_user_becam_board_owner(self, auth_client, user, board_create_data):
        """
        Авторизованный пользователь при создании доски становиться ее владельцем
        """

        response = auth_client.post(self.url, data=board_create_data())

        assert response.status_code == status.HTTP_201_CREATED
        board_participant = BoardParticipant.objects.get(user_id=user.id)
        assert board_participant.board.id == response.data['id']
        assert board_participant.role == BoardParticipant.Role.owner
