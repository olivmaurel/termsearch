from django.conf.urls import include, url

from aggregator import views, customviews

urlpatterns = [
    url(r'^ressources$', views.WebsiteListView.as_view(), name='ressources'),
    url(r'^$', views.home_page, name='index'),
    url(r'^search$', views.term_search, name='search'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact, name='contact'),

    url(r'^proz/(?P<term>\w+)/$', customviews.proz_spider_tester, name='proz'),
    url(r'^termium/(?P<term>\w+)/$', customviews.termium_spider_tester, name='termium'),
    url(r'^iate/(?P<term>\w+)/$', customviews.iate_spider_tester, name='iate'),


    # debugging stuff
    url(r'^safemode$', customviews.safemode_search, name='safemode'),
    url(r'^testnormalhttp$', customviews.test_httpresponse, name='testnormalhttp'),
    url(r'^testjinja$', customviews.test_jinja_generate, name='testjinja'),
    url(r'^teststreaminghttp$', customviews.django_streamingthttp_tester, name='teststreaminghttp'),
    url(r'^timer$', customviews.search_with_timer, name='timer'),
]