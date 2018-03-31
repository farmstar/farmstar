import datetime
from django.utils import timezone
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class STATUS(models.Model):
    UNIX = models.FloatField()
    STATUS = models.BooleanField()
