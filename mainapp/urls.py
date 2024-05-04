from django.urls import path
from . import views

urlpatterns = [
    path('',views.gen,name='gen'),
]
