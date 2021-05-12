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


# class BlogList(ListCreateAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer

# class BlogDetail(RetrieveUpdateDestroyAPIView):
#    permission_classes = (IsOwnerOrReadOnly,)
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer