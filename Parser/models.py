from django.db import models

# Create your models here.


class NEM13(models.Model):
    nmi = models.CharField(max_length=10)
    reading_time = models.DateTimeField('date published')
    serial_number = models.CharField(max_length=12)
    reading_value = models.CharField(max_length=15)
    filename = models.CharField(max_length=255)
