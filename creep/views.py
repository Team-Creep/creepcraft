# from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializer import CreepSerializer
from .models import Creep 

class CreepList(ListCreateAPIView):
  queryset = Creep.objects.all()
  serializer_class = CreepSerializer

class CreepDetail(RetrieveUpdateDestroyAPIView):
  queryset = Creep.objects.all()
  serializer_class = CreepSerializer