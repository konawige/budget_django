from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),
    path('add_new', views.addEntries),
]
    