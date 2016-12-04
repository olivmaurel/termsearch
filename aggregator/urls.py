from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^search$', views.term_search, name='term_search'),
    url(r'^$', views.index, name='index'),
    #url(r'^thanks$', views.thanks, name='thanks'),
    url(r'^results$', views.crawler_results, name='results'),
]