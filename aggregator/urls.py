from django.conf.urls import include, url

from aggregator import views, customviews


urlpatterns = [
    url(r'^search$', views.term_search, name='term_search'),
    url(r'^ressources$', views.WebsiteListView.as_view(), name='ressources'),
    url(r'^$', views.home_page, name='home'),
    url(r'^simplestreamer$', customviews.simplestreamer, name='simplestreamer'), # todo remove after testing
    url(r'^normalhttp$', customviews.normal_httpresponse, name='normalhttp'), # todo remove after testing
    url(r'^mytestsearch$', customviews.mytestsearch, name='mytestsearch'), # todo remove after testing
    url(r'^jinja$', customviews.jinja_tester, name='jinja'), # todo remove after testing
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]