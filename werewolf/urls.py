from django.conf.urls import url
from . import views

app_name = 'werewolf'
urlpatterns = [
    url(r'^$', views.OpenVillageIndexView.as_view(), name='index'),
    url(r'^pal/$', views.PalVillageIndexView.as_view(), name='pal'),
    url(r'^log/$', views.EndVillageIndexView.as_view(), name='log'),
    url(r'^(?P<village_id>[0-9]+)/$', views.VillageView, name='village'),
]
