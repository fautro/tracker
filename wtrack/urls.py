from django.urls import path
from wtrack import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_record/', views.add_record()),
    path('add_record/', views.add_morning_weight()),
    path('add_record/', views.add_evening_weight()),
]