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

from django.http import HttpResponse

def scores(request):
  score_file = open('creepcraft/scores.txt')
  highscores = score_file.readlines()
  score_obj = Creep(highscores=highscores[0])
  score_obj.save()
  return HttpResponse("it's working")


