from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^werewolf/', include('werewolf.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^', include('index.urls'))
]
