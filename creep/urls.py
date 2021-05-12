from django.urls import path
# from .views import HomePageView, AboutView
from .views import CreepList, CreepDetail

# urlpatterns = [
#   path('',HomePageView.as_view(), name='home'),
#   path('about', AboutView.as_view(), name='about')
# ]

urlpatterns = [
  path('', CreepList.as_view(), name='creep_list'),
  path('<int:pk>', CreepDetail.as_view(), name='creep_detail')
]