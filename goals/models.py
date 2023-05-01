from random import choices

from django.db import models
from django.utils import timezone

from core.models import User


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


class GoalCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    created = models.DateTimeField(verbose_name='Дата создания')
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)


class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    title = models.CharField(verbose_name='Название', max_length=255)
    desc = models.TextField(verbose_name='Описание', null=True)
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    deadline = models.DateTimeField(verbose_name='Дедлайн', null=True)
    priority = models.PositiveIntegerField(verbose_name='Приоритет', choices=Priority.choices, default=Priority.medium)
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)
    created = models.DateTimeField(verbose_name='Дата создания')
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class GoalComment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(verbose_name='Дата создания')
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)
