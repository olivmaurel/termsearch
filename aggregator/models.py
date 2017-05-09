from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone

from aggregator.spiders import *

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Language(models.Model):
    name = models.CharField(max_length=30, unique=True)
    code3d = models.CharField(max_length=3)
    code2d = models.CharField(max_length=2)

    def __str__(self):
        return "{} - {}".format(self.code2d.lower(), self.name)

class Website(models.Model):
    DEFAULT_PK=1
    name = models.CharField(max_length=50, unique=True)
    homepage = models.URLField()
    search_url = models.URLField()
    description = RichTextField(default="Enter description")
    languages = models.ManyToManyField(Language)

    # def getLanguages(self):
    #     res = []
    #     for l in self.languages.all():
    #          res.append(l)
    #     return res     

    def __str__(self):
        return self.name

class Domain (models.Model):
    DEFAULT_PK=1
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Term(models.Model):
    name = models.CharField(max_length=300)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Search(models.Model):

    DEFAULT_PK = 1
    keywords = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    
    source_language = models.ForeignKey(Language, default=None, related_name="source_language", on_delete=models.CASCADE)
    target_language = models.ForeignKey(Language, default=None, related_name="target_language", on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    domains = models.ManyToManyField(Domain)


    def __str__(self):
        return "\"{}\" ({} > {}) on {}".format(self.keywords, self.source_language, self.target_language, self.website)

    def get_or_create_manytomanys(self, page_record):
        terms, translations, domains = [], [], []

        # for each term in a page_record, get or create in db, append to terms list
        for term in page_record['terms']:
            t, created = Term.objects.get_or_create(name=term, language=self.source_language)
            terms.append(t)
            logger.debug("term : {}\n created : {} \n".format(term, created))
        # for each translation in a page_record, get or create in db, append to translations list
        for translation in page_record['translations']:
            t, created = Term.objects.get_or_create(name=translation, language=self.target_language)
            logger.debug("translation : {}\n created : {} \n".format(translation, created))
            translations.append(t)
        # for each domain in a page_record
        for domain in page_record['domain']:
            dom, created = Domain.objects.get_or_create(name=domain)
            logger.debug("domain: {}\n created : {}".format(domain, created))
            domains.append(dom)

        return terms, translations, domains

    def get_records_from_scrapy(self):
        """
        The twited Reactor used by scrapy doesn't work well with WSGI/Django, so Scrapydo is needed
        to call scrapy more than once and get the scraping results as a list of scrapy.items.record objects

        """
        scrapydo.setup()

        logger.debug("Now sending HTTP request to get results from {}".format(self.website))

        search_parameters = {
            'keywords': self.keywords,
            'source_language': self.source_language,
            'target_language': self.target_language
        }

        spider_results = scrapydo.run_spider(self.get_spider_from_scrapy(search_parameters), **search_parameters)
        # todo delete this method when scrapy is deleted
        return spider_results

    def get_records(self):
        # dont use this # todo delete this method
        spider = self.get_spider()

        page_results = []
        response = requests.get(spider.url)
        for record in spider.parse(response):
            page_results.append(record)

        return page_results

    def get_spider(self):
        search_parameters = {
            'keywords': self.keywords,
            'source_language': self.source_language,
            'target_language': self.target_language}

        # todo test dict performance versus elif switch-like statement
        return {'iate': IateSpider(**search_parameters),
                'proz': ProzSpider(**search_parameters),
                'termium': TermiumSpider(**search_parameters)}[self.website.name.lower()]

    def get_spider_from_scrapy(self, search_parameters):

        from aggregator.scraper import scrapy_spiders

        return {'iate': scrapy_spiders.IateSpider(**search_parameters),
                'proz': scrapy_spiders.ProzSpider(**search_parameters),
                'termium': scrapy_spiders.TermiumSpider(**search_parameters)}[self.website.name.lower()]

    def save_results_in_db(self, page_results):

        for record in page_results:
            self.create_record(record)


    def create_record(self, record):
        '''
        :param search: django.models.Search
        :param record: scrapy.items.Record
        :return: django.models.Record
        creates a new Record object using Record.objects.create()
        adds terms and translations as a list (Manytomany

        '''
        new_record = Record.objects.create(search=self)
        # list of Term objects (terms, translations, domains) to save in Record
        terms, translations, domains = self.get_or_create_manytomanys(record)
        new_record.terms.add(*terms)
        new_record.translations.add(*translations)
        new_record.domains.add(*domains)

        return record


class Record(models.Model):
    terms = models.ManyToManyField(Term, related_name="terms")
    translations = models.ManyToManyField(Term, related_name="translations")
    last_update = models.DateTimeField(default=timezone.now)
    domains = models.ManyToManyField(Domain)
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    # result_url = models.URLField()


    def __str__(self):
        terms_list = [term.name for term in self.terms.all()]
        translations_list = [translation.name for translation in self.translations.all()]
        domains_list = [domain.name for domain in self.domains.all()]
        return "***\nterms:{}\ntranslations:{}\ndomains:{}\nsource:{}\n***\n".format(terms_list,
                                                                        translations_list,
                                                                        domains_list,
                                                                        self.search.website.name)


