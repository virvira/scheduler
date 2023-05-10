from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import Board, BoardParticipant


@pytest.fixture()
def board_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data
    return _wrapper


@pytest.mark.django_db()
class TestBoardCreateView:
    url = reverse('create-board')

    def test_auth_required(self, client, board_create_data):
        """
        При создании доски неавторизованный пользователь получит ошибку доступа
        """
        response = client.post(self.url, data=board_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_board(self, auth_client, board_create_data):
        """
        При создании удаленной доски пользователь получит ошибку
        """
        response = auth_client.post(self.url, data=board_create_data(is_deleted=True))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['is_deleted'] is False
        assert Board.objects.last().is_deleted is False

    def test_request_user_became_board_owner(self, auth_client, user, board_create_data):
        """
        Пользователь, создавший доску, становится ее владельцем
        """
        response = auth_client.post(self.url, data=board_create_data())
        board_participant = BoardParticipant.objects.get(user_id=user.id)
        assert response.status_code == status.HTTP_201_CREATED
        assert board_participant.board_id == response.data['id']
        assert board_participant.role == BoardParticipant.Role.owner
