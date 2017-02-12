from django.conf.urls import include, url

from aggregator import views

urlpatterns = [
    url(r'^search$', views.term_search, name='term_search'),
    url(r'^ressources$', views.WebsiteListView.as_view(), name='ressources'),
    url(r'^$', views.home_page, name='home'),
    url(r'^streamer$', views.streamer, name='streamer'),
    url(r'^simplestreamer$', views.simplestreamer, name='simplestreamer'), # todo remove after testing
    url(r'^normalhttp$', views.normal_httpresponse, name='normalhttp'),
    # url(r'^results$', views.crawler_results, name='results'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]