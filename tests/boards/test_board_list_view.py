import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from goals.serializers import BoardCreateSerializer
from tests.factories import BoardFactory, UserFactory


@pytest.mark.django_db
class TestBoardsList:
    url = reverse('board-list')

    def test_get_list_unauthorized(self, client):
        """
        Неавторизированный пользователь получает ошибку при запросе списка boards
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list_of_boards_not_participant(self, auth_client, board_factory):
        """
        Авторизованный пользователь не является участником ни одной доски и получает пустой список
        """
        board_factory.create_batch(size=2)
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_list_success(self, auth_client, board_factory, user):
        """
        Авторизованный пользователь получает список boards, в котором является участником
        """
        boards = board_factory.create_batch(size=2, with_owner=user)
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for board in BoardCreateSerializer(boards, many=True).data:
            assert board in response.data
