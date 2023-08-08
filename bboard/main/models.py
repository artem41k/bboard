from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        'Прошёл активацию?', default=True, db_index=True
    )
    send_messages = models.BooleanField(
        'Получать оповещения о новых комментариях?', default=True
    )

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    name = models.CharField(
        'Название', max_length=20, db_index=True, unique=True
    )
    order = models.PositiveSmallIntegerField(
        'Порядок', db_index=True, default=0
    )
    super_rubric = models.ForeignKey(
        'SuperRubric', on_delete=models.PROTECT, null=True,
        blank=True, related_name='rubrics', verbose_name='Надрубрика'
    )


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = (
            'super_rubric__order', 'super_rubric__name',
            'order', 'name',
        )
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'
