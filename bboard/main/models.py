from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        "Прошёл активацию?", default=True, db_index=True
    )
    send_messages = models.BooleanField(
        "Получать оповещения о новых комментариях?", default=True
    )

    class Meta(AbstractUser.Meta):
        pass
