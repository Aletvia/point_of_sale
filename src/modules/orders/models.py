import json
from django.db import models


class Order(models.Model):
    items = models.JSONField(default={})
    total = models.IntegerField(default=0)