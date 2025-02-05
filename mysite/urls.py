from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='view_all'),
    path('add_new', views.addEntries, name='add_new'),
    path('confirm/<int:intBank>', views.ConfirmEntries, name='confirm'),
    path('create/', views.ItemCreateView.as_view(), name='create_item'),
]
    