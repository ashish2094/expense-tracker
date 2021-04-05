from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length = 100)

    def __str__(self):
        return self.source

    class Meta:
        ordering: ['-date']

class Source(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Sources'