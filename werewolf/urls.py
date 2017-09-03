from django.conf.urls import url
from . import views

app_name = 'werewolf'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<village_id>[0-9]+)/$', views.village, name='village'),
]
