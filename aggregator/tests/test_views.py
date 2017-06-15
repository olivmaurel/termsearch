from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from aggregator import views


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)


    def test_search_page_returns_correct_html(self):

        response = self.client.get('/aggregator/search')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Termsearch Aggregator</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'aggregator/search_home.html')


    def test_news_releases_pages_opens(self):

        response = self.client.get('/news/releases/')

        self.assertTemplateUsed(response, 'news/releases.html')