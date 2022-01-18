from django.db import models

# Create your models here.
class Exchanges(models.Model):
  page = models.CharField(max_length=100)
  exchange = models.CharField(max_length=100)
  currency = models.CharField(max_length=100)
  date = models.DateTimeField(auto_now_add=True)
