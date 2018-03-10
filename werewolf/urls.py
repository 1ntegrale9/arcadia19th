from django.urls import path
from . import views

app_name = 'werewolf'
urlpatterns = [
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('charaset/', views.CharasetView.as_view(), name='charaset'),
    path('create/', views.CreateVillageView.as_view(), name='create'),
    path('open/', views.OpenVillageIndexView.as_view(), name='open'),
    path('game/', views.StartVillageIndexView.as_view(), name='game'),
    path('log/', views.EndVillageIndexView.as_view(), name='log'),
    path('pal/', views.PalVillageIndexView.as_view(), name='pal'),
    path('<int:village_id>/', views.VillageView, name='village'),
]
