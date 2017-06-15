from django.conf.urls import url

from news import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^releases$', views.releases, name='releases'),
    url(r'^todo$', views.todopage, name='todo'),
]