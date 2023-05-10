import factory
from django.utils import timezone
from pytest_factoryboy import register

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # return cls._get_manager(model_class).create_user(*args, **kwargs)
        return User.objects.create_user(*args, **kwargs)


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)


@register
class BoardFactory(DatesFactoryMixin):
    class Meta:
        model = Board

    title = factory.Faker('sentence')

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class CategoryFactory(DatesFactoryMixin):
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    board = factory.SubFactory(BoardFactory)

    class Meta:
        model = GoalCategory


@register
class GoalFactory(DatesFactoryMixin):
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker('sentence')

    class Meta:
        model = Goal


@register
class GoalCommentFactory(DatesFactoryMixin):
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence')

    class Meta:
        model = GoalComment
