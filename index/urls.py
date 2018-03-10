from django.conf.urls import url
from . import views

app_name = 'index'
urlpatterns = [
    url(r'^$', views.WelcomePageView.as_view(), name='welcome'),
]
