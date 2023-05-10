from typing import Any
from unittest.mock import ANY

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from goals.models import GoalComment, Goal


@pytest.mark.django_db
class TestCommentCreateView:
    url = reverse('create-comment')

    def test_create_unauthorized(self, client, faker) -> None:
        """
        Неавторизованный пользователь пытается создать комментарий и получает ошибку доступа
        """
        response = client.post(self.url, data={})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # def test_create_success(self, auth_client: APIClient, goal: Goal) -> None:
    #     """
    #     Успешное создание комментария
    #     """
    #     response = auth_client.post(self.url, data={
    #         'text': 'Test comment',
    #         'goal': goal.id
    #     })
    #     goal_comment = GoalComment.objects.last()
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert response.json() == {
    #         'id': goal_comment.id,
    #         'created': ANY,
    #         'updated': ANY,
    #         'text': 'Test comment',
    #         'goal': goal_comment.goal.id
    #     }
