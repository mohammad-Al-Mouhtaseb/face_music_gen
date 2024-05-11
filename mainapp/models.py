from django.db import models
from django.utils import timezone

# Create your models here.

class Music(models.Model):
    doctor = models.EmailField(blank=True, default='')
    patient = models.EmailField(blank=True, default='')
    music_path = models.FilePathField(null=True, blank=True)
    type = models.CharField(max_length=50,default='',null=True, blank=True)