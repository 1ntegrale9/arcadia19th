from django.conf.urls import url
from . import views

app_name = 'index'
urlpatterns = [
    url(r'^$', views.WelcomePageView.as_view(), name='welcome'),
    url(r'^about$', views.AboutPageView.as_view(), name='top'),
    url(r'^charaset$', views.CharasetView.as_view(), name='charaset'),
]
