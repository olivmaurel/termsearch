from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class SimpleSearchTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_termsearch_and_read_the_results(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000/aggregator/search')

        # She notices the page title and header mention to-do lists
        self.assertIn('Termsearch', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Termsearch', header_text)



        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list

if __name__ == '__main__':
    unittest.main(warnings='ignore')