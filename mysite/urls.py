from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('index.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^werewolf/', include('werewolf.urls')),
    url(r'^bbs/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
]
