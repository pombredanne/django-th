# coding: utf-8
from django.db import models
from django_th.models.services import Services
import uuid


class Rss(Services):
    """
        Model for RSS Service
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=255)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_rss'

    def __str__(self):
        return self.url

    def show(self):
        return "Services RSS {} {}".format(self.url, self.trigger)
