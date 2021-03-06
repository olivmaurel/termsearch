import logging
import json
import time
from lxml import html
import requests

logger = logging.getLogger(__name__)


class GenericSpider(object):

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = keywords
        self.name = "generic"
        self.source_language = source_language
        self.target_language = target_language
        self.url = ""
        self.xpath_for_results = "" # xpath to be set in each subclass

    def sanitize_result_string(self, text):

        return text.replace('\xa0', '').replace('\"', '')

    def get_results_as_list(self):

        results_list = []

        for record in self.parse():
            results_list.append(record)

        return results_list

    def get_html_tree(self, response):

        return html.fromstring(response.content)


    def record_template(self):

        record = {'website': self.name,
                     'source_language':self.source_language,
                     'target_language':self.target_language}

        return record

    def create_record(self, result):

        return self.record_template() # default method to be overriden by each specific spider

    def parse(self, response=None):

        if response is None:
            response = requests.get(self.url)
        page_results = self.get_page_results(response, self.xpath_for_results)

        if not page_results:
            yield self.no_results()
        for result in page_results:
            yield self.create_record(result)

    def get_page_results(self, response, xpath):

        html_tree = self.get_html_tree(response)
        return  html_tree.xpath(xpath)

    def no_results(self):

        no_result = self.record_template()
        no_result['error'] ='No results from {}'.format(self.name)

        return no_result


class IateSpider(GenericSpider):

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(keywords, source_language, target_language, *args, **kwargs)
        # 'keywords' inherited from GenericSpider
        # IATE uses 2 digits language codes 'en', 'fr, 'it' etc
        self.source_language = source_language.code2d
        self.target_language = target_language.code2d
        self.name = "iate"
        self.url = 'http://iate.europa.eu/SearchByQuery.do?' \
                    'method=search&query={}&sourceLanguage={}' \
                    '&targetLanguages={}&domain=0' \
                    '&matching=&typeOfSearch=s'.format(self.keywords, self.source_language, self.target_language)
        self.xpath_for_results = '//div[@id="searchResultBody"]/table'

    def parse(self, url=None):

        if url is None:
            url = self.url

        response = requests.get(url)

        page_results = self.get_page_results(response, self.xpath_for_results)

        if not page_results:

            yield self.no_results()

        for result_table in page_results:
            result = result_table.xpath('./tr')

            record = self.create_record(result)

            if record is not None:
                yield record


    def create_record(self, result):

        record = self.record_template()
        # each result is a html table with 3+ tr tags
        # first tr is the domain
        # second tr starts with source_language.upper
        # every following tr is a source terms until we have a tr starting with target_language.upper
        # then, every following tr is a translation term
        record['domain'] = self.get_domains(result)
        record['terms'], record['translations'] = self.get_terms_and_translations(result)
        return record

    def get_domains(self, result):
        """
        truncate the unnecessary part at the end of the domain string
        by deleting everything starting from the [ character (and -1 for the extra whitespace)
        returns a list of strings
        # >>> get_domains(['TECHNICAL, AGRICULTURE, FORESTRY AND FISHERIES [EP] Full entry'])
        # ['TECHNICAL', 'AGRICULTURE, FORESTRY AND FISHERIES']
        """
        text = result[0].xpath('normalize-space(.)')

        text = text[:text.index('[')-1]
        domains = text.split(', ')
        return domains

    def get_terms_and_translations(self, result):
        """
        the [0] item is always the domain in the IATE result table
        the [1] item is always a source in the IATE result table
        truncate the "EN " at the beginning of the string and add to the list
        """
        terms = [result[1].xpath('normalize-space(.)')[3:]]
        translations = []
        term_is_a_translation = False

        # then loop through all the remaining <tr> tags in the table, starting from [2]
        for item in result[2:]:

            item = item.xpath('normalize-space(.)')

            if item[0:3] == self.target_language.upper() + " ":
                # if the string starts with target_language, then stop and return the result
                translations.append(item[3:])
                term_is_a_translation = True

            elif term_is_a_translation:
                translations.append(item)
            else:
                terms.append(item)

        return terms, translations


class ProzSpider(GenericSpider):

    def __init__(self, keywords, source_language, target_language, *args,  **kwargs):

        super().__init__(keywords, source_language, target_language, *args, **kwargs)
        # 'keywords' inherited from GenericSpider
        # proz uses 3 digits language codes 'eng', 'fra, 'ita' etc
        self.source_language = source_language.code3d
        self.target_language = target_language.code3d
        self.name = "proz"
        self.url = 'http://www.proz.com/ajax/ajax_search.php'
        self.xpath_for_results = '//tbody[@class=\'search_result_body\']/tr/td[4]'

        self.formdata = {   'action': 'term_search',
                            'search_params[term]': self.keywords,
                            'search_params[from]': self.source_language,
                            'search_params[to]': self.target_language,
                            'search_params[bidirectional]': 'true',
                            'search_params[results_per_page]': '100'}

    def parse(self, response=None):

        if response is None:
            response = requests.post(self.url, data=self.formdata)

        return super(ProzSpider, self).parse(response)

    def create_record(self, result):

        record = self.record_template()
        record['domain'] = self.get_domains(result)
        record['terms'], record['translations'] = self.get_terms_and_translations(result)

        return record

    def get_terms_and_translations(self, result):

        terms = [result.xpath('normalize-space(string(./a))')]
        translations = [result.xpath('normalize-space(string(./a[2]))')]

        return terms, translations


    def get_page_results(self, response, xpath):

        html_tree = html.fromstring(json.loads(response.text)['html'])
        return html_tree.xpath(xpath)

    def get_domains(self, result):
        """
        takes a single string containing all the domains for the result,
        removes the double quotes in it, and split it in a list of strings,
        one string per domain

        # >>> result = ['Tech/Engineering>Computers(general);
                    Engineering(general);
                    IT(InformationTechnology)>"Wordnet";
                    "Finance/Business";
                    "Automotive Glossary (Chrysler Terminology) English/Portuguese (BRAZIL)"']

        # >>> ProzSpider.get_domains(result)

        ['Tech/Engineering>Computers(general)',
            ' Engineering(general)',
            ' IT(InformationTechnology)>Wordnet',
            ' Finance/Business',
            ' Automotive Glossary (Chrysler Terminology) English/Portuguese (BRAZIL)']


        """
        domain = result.xpath('normalize-space(string(../td[3]))')
        # remove quotation marks and /xa0 unicode crap
        domain = self.sanitize_result_string(domain)

        return domain.split('>')


class TermiumSpider (GenericSpider):

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(keywords, source_language, target_language, *args, **kwargs)
        # 'keywords' inherited from GenericSpider
        # termium uses 2 digits language codes 'en', 'fr, 'it' etc
        self.source_language = source_language.code2d
        self.target_language = target_language.code2d
        self.name = "termium"
        self.url = 'http://www.btb.termiumplus.gc.ca/tpv2alpha/' \
                         'alpha-eng.html?lang=eng&srchtxt={}'.format(keywords)
        self.xpath_for_results =  '//div[@id=\'resultrecs\']/' \
                                  'section[contains(normalize-space(@class), \'recordSet\')]/div'

    def create_record(self, result):

        record = self.record_template()
        record['domain'] = self.get_domains(result)
        record['terms']  = self.get_terms(self.source_language, result)
        record['translations'] = self.get_terms(self.target_language, result)

        return record

    def get_domains(self, result):
        '''
        :param record: a SelectorList from main results table ('tables' in parse() )
        :return: a list of strings of every dom  ain included in the record
        '''
        domains_list = result.xpath('div[@class=\'col-md-4\']/section/div/section[@lang=\'en\']'
                            '/div/ul//li[@class=\'small\']')

        return [domain.xpath('normalize-space(.)') for domain in domains_list]

    def get_terms(self, language, result):

        terms = []

        # clean up the useless content, everything from " \xa0" on should be removed
        for term in result.xpath('div[@class=\'col-md-4\']/section/div/div[@lang=\'{}\']/ul'
                                   '/li[contains(@class,\'text-primary\')]'.format(language)):

            term = term.xpath('normalize-space(.)')
            terms.append(term[:term.index('\xa0') - 1])

        return terms