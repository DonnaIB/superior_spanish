from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('short_stories', views.short_stories, name='short_stories'),
    path('recorded_lessons', views.recorded_lessons, name='recorded_lessons'),

]
