from django.conf.urls import include, url

from aggregator import views, customviews


urlpatterns = [
    url(r'^ressources$', views.WebsiteListView.as_view(), name='ressources'),
    url(r'^$', views.home_page, name='home'),
    url(r'^search$', views.term_search, name='search'),
    url(r'^anothertest$', customviews.fix_the_template_mess, name='anothertest'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]