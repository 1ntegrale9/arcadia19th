from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^', include('werewolf.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^index/', include('index.urls'))
]
