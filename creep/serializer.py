from rest_framework import serializers
from .models import Creep

class CreepSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ['id', 'user', 'name', 'highscores']
    model = Creep