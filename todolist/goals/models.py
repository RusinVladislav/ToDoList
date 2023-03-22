from django.db import models
from django.utils import timezone

from todolist.core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    class Meta:
        abstract = True


class GoalCategory(BaseModel):

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return f'{self.title} <{self.user.username}>'


class Goal(BaseModel):

    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, "В архиве"

    class Priority(models.IntegerChoices):
        low = 1, 'L'
        medium = 2, 'M'
        high = 3, 'H'
        critical = 4, 'C'

    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(to=GoalCategory, on_delete=models.PROTECT, related_name='goals')
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='Автор')
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.medium)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"


class GoalComment(BaseModel):
    text = models.TextField(null=True, blank=True)
    goal = models.ForeignKey(to=Goal, on_delete=models.PROTECT, verbose_name='Цель')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
