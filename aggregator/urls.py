from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^search$', views.term_search, name='term_search'),
    # url(r'^results$', views.search_results, name='search_results'),
    url(r'^$', views.index, name='index'),
    # url(r'^streamer$', views.streamer, name='streamer'),
    # url(r'^results$', views.crawler_results, name='results'),
]