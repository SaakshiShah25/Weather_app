from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('delete/<city_name>/',views.delete,name='delete'),
]
