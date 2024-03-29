from random import choices

from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name='Дата создания')
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Priority(models.IntegerChoices):
    low = 1, 'Низкий'
    medium = 2, 'Средний'
    high = 3, 'Высокий'
    critical = 4, 'Критический'


class Status(models.IntegerChoices):
    to_do = 1, 'К выполнению'
    in_progress = 2, 'В процессе'
    done = 3, 'Выполнено'
    archived = 4, 'Архив'


class Board(DatesModelMixin):
    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)


class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    class Role(models.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    board = models.ForeignKey(
        Board,
        verbose_name='Доска',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    role = models.PositiveSmallIntegerField(
        verbose_name='Роль', choices=Role.choices, default=Role.owner
    )


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    board = models.ForeignKey(
        Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='categories'
    )
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    title = models.CharField(verbose_name='Название', max_length=255)
    desc = models.TextField(verbose_name='Описание', null=True)
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    due_date = models.DateTimeField(verbose_name='Дедлайн', null=True)
    priority = models.PositiveIntegerField(verbose_name='Приоритет', choices=Priority.choices, default=Priority.medium)
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
