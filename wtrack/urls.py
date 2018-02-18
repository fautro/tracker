from django.urls import path
from wtrack import views

urlspatterns = [
    path('', views.index, name='index'),
]