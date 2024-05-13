from django.urls import path
from . import views

urlpatterns = [
    path('gen',views.gen,name='gen'),
    path('get_music',views.get_music,name='get_music'),
    path('get_my_list',views.get_my_list,name='get_my_list'),
    path('get_folder_list',views.get_folder_list,name='get_folder_list'),
    path('surahList',views.surahList,name='surahList'),
    path('surah_audio/<str:name>',views.surah_audio,name='surah_audio'),
]
