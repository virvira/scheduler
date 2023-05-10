import pytest
from django.urls import reverse
from rest_framework import status
from goals.serializers import GoalCommentSerializer


@pytest.mark.django_db
class TestCommentListView:
    url = reverse('comment-list')

    def test_get_list_unauthorized(self, client):
        """
        Неавторизированный пользователь запрашивает список комментариев и получает ошибку
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list(self, auth_client, goal, goal_comment_factory):
        """
        Авторизованный пользователь запрашивает список комментариев
        """
        comments = goal_comment_factory.create_batch(2, goal=goal)
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for comment in GoalCommentSerializer(comments, many=True).data:
            assert comment in response.data
