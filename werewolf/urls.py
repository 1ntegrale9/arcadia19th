from django.urls import path
from . import views

app_name = 'werewolf'
urlpatterns = [
    path('open/', views.OpenVillageIndexView.as_view(), name='index'),
    path('pal/', views.PalVillageIndexView.as_view(), name='pal'),
    path('log/', views.EndVillageIndexView.as_view(), name='log'),
    path('<int:village_id>/', views.VillageView, name='village'),
]
