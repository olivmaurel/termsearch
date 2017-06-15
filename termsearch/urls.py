from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = [

    url(r'^news/', include('news.urls',namespace="news")),
    url(r'^', include('aggregator.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
