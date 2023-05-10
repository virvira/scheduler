import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from goals.models import Board, GoalCategory
from goals.serializers import GoalCategorySerializer
from tests.factories import CategoryFactory


@pytest.mark.django_db
class TestCategoryList:
    url = reverse('category-list')

    def test_get_list_unauthorized(self, client):
        """
        Неавторизированный пользователь получает ошибку при запросе списка категорий
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list(self, auth_client, board, category_factory):
        """
        Авторизованный пользователь получает список категорий
        """
        board, category = board
        categories = category_factory.create_batch(2, board=board)

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for category in GoalCategorySerializer(categories, many=True).data:
            assert category in response.data
