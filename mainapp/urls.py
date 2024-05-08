from django.urls import path
from . import views

urlpatterns = [
    path('gen/<str:text>',views.gen,name='gen'),
    path('get/<str:text>',views.get,name='get'),
]
