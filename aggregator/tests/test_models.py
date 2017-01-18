from django.test import TestCase
from django.db import IntegrityError
from django.db.utils import DataError


from aggregator.models import Website, Language

import requests

class WebsiteTestCase(TestCase):

    fixtures = ['language.json','website.json']

    def setUp(self):
        pass

    def test_website_sends_back_HTTP200(self):

        for w in Website.objects.all():

            try:
                response = requests.get(w.search_url)
            except ConnectionError:
                return False
            assert response.status_code == 200

    def test_unique_name_constraint(self):

        with self.assertRaises(IntegrityError):
            Website.objects.create(name="proz")

    def test_name_length_constraint(self):

        with self.assertRaises(DataError):
            Website.objects.create(name="test"*2400) # long string



class LanguageTestCase(TestCase):

    fixtures = ['language.json', 'website.json']

    def setUp(self):
        pass

    def test_unique_name_constraint(self):

        with self.assertRaises(IntegrityError):
            Language.objects.create(name="English")

    def test_name_length_constraint(self):

        with self.assertRaises(DataError):
            Language.objects.create(name="test"*2400) # long string
