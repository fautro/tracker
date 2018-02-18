from django.urls import path
from wtrack import views

urlspatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]