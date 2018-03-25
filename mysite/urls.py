from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('index.urls')),
    path('account/', include('account.urls')),
    path('werewolf/', include('werewolf.urls')),
    path('bbs/', include('blog.urls')),
    path('admin/', admin.site.urls),
]
