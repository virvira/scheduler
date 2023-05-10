import pytest
from django.urls import reverse
from rest_framework import status
from goals.serializers import GoalSerializer


@pytest.mark.django_db
class TestGoalsListView:
    url = reverse('goal-list')

    def test_get_list_unauthorized(self, client) -> None:
        """
        Неавторизированный пользователь получает ошибку при запросе списка целей
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list_success(self, auth_client, board, goal_factory) -> None:
        """
        Авторизованный пользователь получает список целей
        """
        _, category = board
        goals = goal_factory.create_batch(2, category=category)

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for goal in GoalSerializer(goals, many=True).data:
            assert goal in response.data
