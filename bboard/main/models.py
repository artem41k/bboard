from django.db import models
from django.contrib.auth.models import AbstractUser

from .utilities import get_timestamp_path, send_new_comment_notification


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        'Прошёл активацию?', default=True, db_index=True
    )
    send_messages = models.BooleanField(
        'Получать оповещения о новых комментариях?', default=True
    )

    class Meta(AbstractUser.Meta):
        pass

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)


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

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'

    def __str__(self):
        return self.name


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    class Meta:
        proxy = True
        ordering = (
            'super_rubric__order', 'super_rubric__name',
            'order', 'name',
        )
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)


class Bb(models.Model):
    rubric = models.ForeignKey(
        SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика'
    )
    title = models.CharField('Название', max_length=40)
    content = models.TextField('Описание')
    price = models.PositiveIntegerField('Цена')
    contacts = models.TextField('Контакты')
    image = models.ImageField(
        'Изображение', blank=True, upload_to=get_timestamp_path
    )
    author = models.ForeignKey(
        AdvUser, on_delete=models.CASCADE, verbose_name='Автор'
    )
    is_active = models.BooleanField('Активно', default=True, db_index=True)
    created_at = models.DateTimeField(
        'Опубликовано', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-created_at',)

    def delete(self, *args, **kwargs):
        for add_img in self.additionalimage_set.all():
            add_img.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


class AdditionalImage(models.Model):
    bb = models.ForeignKey(
        Bb, on_delete=models.CASCADE, verbose_name='Объявление'
    )
    image = models.ImageField("Изображение", upload_to=get_timestamp_path)

    class Meta:
        verbose_name = 'Дополнительное изображение'
        verbose_name_plural = 'Дополнительные изображения'


class Comment(models.Model):
    bb = models.ForeignKey(
        Bb, verbose_name='Объявление',
        on_delete=models.CASCADE
    )
    author = models.CharField('Автор', max_length=30)
    content = models.TextField('Содержание')
    is_active = models.BooleanField('Активен', db_index=True, default=True)
    created_at = models.DateTimeField(
        'Опубликован', db_index=True, auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    instance = kwargs['instance']
    author = instance.bb.author
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(instance)


models.signals.post_save.connect(
    post_save_dispatcher,
    sender=Comment
)
