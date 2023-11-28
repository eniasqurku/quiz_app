import json

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class LogEntryManager(models.Manager):
    use_in_migrations = True

    def log_action(
        self,
        user_id,
        content_type_id,
        object_id,
        object_repr,
        action_flag,
        change_message="",
    ):
        if isinstance(change_message, list):
            change_message = json.dumps(change_message)
        self.model.objects.create(
            user_id=user_id,
            content_type_id=content_type_id,
            object_id=object_id,
            object_repr=object_repr[:200],
            action_flag=action_flag,
            change_message=change_message,
        )


class ActionLogger(models.Model):
    class Meta:
        verbose_name = "Action Logger"
        verbose_name_plural = "Action Loggers"
        db_table = "action_logger"

    action_time = models.DateTimeField(
        "Action time", default=timezone.now, editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, verbose_name="User", null=True
    )
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, verbose_name="Content Type", blank=True, null=True
    )
    object_id = models.TextField("Object id", blank=True)
    object_repr = models.CharField("Object repr", max_length=200)
    action_flag = models.PositiveSmallIntegerField("Action flag")
    change_message = models.TextField("Change message", blank=True)
    objects = LogEntryManager()
