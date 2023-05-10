from unittest.mock import ANY

import pytest
from django.urls import reverse
from rest_framework import status
from goals.models import Goal


@pytest.mark.django_db
class TestGoalCreateView:
    url = reverse('create-goal')

    def test_create_unauthorized(self, client):
        """
        При создании цели неавторизованный пользователь получит ошибку доступа
        """
        response = client.post(self.url, data={})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_success(self, auth_client, board):
        """
        Успешное создание цели
        """
        board, category = board
        response = auth_client.post(self.url, data={
            'category': category.id,
            'title': 'Test title'
        })

        goal = Goal.objects.last()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': goal.id,
            'category': category.id,
            'created': ANY,
            'updated': ANY,
            'title': 'Test title',
            'desc': goal.desc,
            'due_date': goal.due_date,
            'status': goal.status,
            'priority': goal.priority
        }
