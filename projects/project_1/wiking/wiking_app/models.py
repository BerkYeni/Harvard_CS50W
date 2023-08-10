from django.db import models

# Create your models here.
class Entry(models.Model):
  title = models.CharField(max_length=64, unique=True)
  content = models.CharField(max_length=1024)