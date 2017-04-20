import logging
import json
from lxml import html

logger = logging.getLogger(__name__)


class GenericSpider(object):

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = keywords
        self.source_language = source_language
        self.target_language = target_language

    def sanitize_result_string(self, text):

        return text.replace('\xa0', '').replace('\"', '')

    def get_results_as_list(self, response):

        results_list = []

        for record in self.parse(response):
            results_list.append(record)

        return results_list


class IateSpider(GenericSpider):

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(keywords, source_language, target_language, *args, **kwargs)
        # 'keywords' inherited from GenericSpider
        # IATE uses 2 digits language codes 'en', 'fr, 'it' etc
        self.source_language = source_language.code2d
        self.target_language = target_language.code2d

        self.url = 'http://iate.europa.eu/SearchByQuery.do?' \
                    'method=search&query={}&sourceLanguage={}' \
                    '&targetLanguages={}&domain=0' \
                    '&matching=&typeOfSearch=s'.format(self.keywords, self.source_language, self.target_language)

    def parse(self, response):

        html_tree = html.fromstring(response.content)

        results_list = html_tree.xpath('//div[@id="searchResultBody"]/table')

        for result_table in results_list:
            result = result_table.xpath('./tr')
            yield self.get_record(result)

        # crawl the next page if more than 10 results
        for f in html_tree.xpath('//div[@id="searchResultFooter"]//*'):
            res = f.xpath('normalize-space(.)')
            if res == ['>']:
                # todo: crawl every page when more than 10 pages
                next_page = ''.join(f.xpath('normalize-space(./@href)'))
                yield self.parse(next_page)




    def get_record(self, result):

        record = dict()

        record['website'] = "IATE"
        record['source_language'] = self.source_language
        record['target_language'] = self.target_language
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
        self.url = 'http://www.proz.com/ajax/ajax_search.php'
        self.formdata = {   'action': 'term_search',
                            'search_params[term]': self.keywords,
                            'search_params[from]': self.source_language,
                            'search_params[to]': self.target_language,
                            'search_params[bidirectional]': 'true',
                            'search_params[results_per_page]': '100'}

    def parse(self, response):

        html_tree = html.fromstring(json.loads(response.text)['html'])

        results_list = html_tree.xpath('//tbody[@class=\'search_result_body\']/tr/td[4]')

        for result in results_list:

            yield self.get_record(result)


    def get_record(self, result):

        record = dict()

        record['website'] = "proz"
        record['source_language'] = self.source_language
        record['target_language'] = self.target_language
        record['domain'] = self.get_domains(result)
        record['terms'], record['translations'] = self.get_terms_and_translations(result)

        return record

    def get_terms_and_translations(self, result):

        terms = result.xpath('normalize-space(string(./a))')
        translations = result.xpath('normalize-space(string(./a[2]))')

        return terms, translations

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