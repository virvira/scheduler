import factory
from django.utils import timezone
from pytest_factoryboy import register

from core.models import User
from goals.models import Board


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
