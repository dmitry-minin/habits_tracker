from django.urls import path
from .views import HabitViewSet
from rest_framework.routers import DefaultRouter

app_name = 'habits'
router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habits')

urlpatterns =[

] + router.urls
