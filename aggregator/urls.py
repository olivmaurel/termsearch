from django.conf.urls import include, url

from aggregator import views, customviews


urlpatterns = [
    url(r'^ressources$', views.WebsiteListView.as_view(), name='ressources'),
    url(r'^$', views.home_page, name='home'),
    url(r'^search$', views.term_search, name='search'),
    url(r'^normalhttp$', customviews.termsearchnormalhttp, name='searchnormalhttp'),
    url(r'^anothertest$', customviews.jinja_tester, name='anothertest'),
    url(r'^proz/(?P<term>\w+)/$', customviews.proz_spider_tester, name='proz'),
    url(r'^termium/(?P<term>\w+)/$', customviews.termium_spider_tester, name='termium'),
    url(r'^iate/(?P<term>\w+)/$', customviews.iate_spider_tester, name='iate'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]