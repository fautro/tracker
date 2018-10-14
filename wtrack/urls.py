from django.urls import path
from wtrack import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_record/', views.add_record, name='add_record'),
    path('test/', views.test, name='test'),
]