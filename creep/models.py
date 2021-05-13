from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model


class Creep(models.Model):
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  name = models.CharField(max_length=64)
  highscores = models.IntegerField(max_length=None)

  def __str__(self):
    return self.name



