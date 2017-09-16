from django.conf.urls import url
from . import views

app_name = 'account'
urlpatterns = [
    url(r'^mypage/$', views.MyPageView.as_view(), name='mypage'),
    url(r'^create/$', views.CreateUserView.as_view(), name='create'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
