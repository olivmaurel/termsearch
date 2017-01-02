from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class Language(models.Model):
    name = models.CharField(max_length=30)
    code3d = models.CharField(max_length=3)
    code2d = models.CharField(max_length=2)

    def __str__(self):
        return "{} - {}".format(self.code2d.upper(), self.name)

class Website(models.Model):
    DEFAULT_PK=1
    name = models.CharField(max_length=50)
    homepage = models.URLField()
    search_url = models.URLField()
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

    def get_or_create_manytomanys(self, record):
        terms, translations, domains = [], [], []

        # for each term in a record, get or create in db, append to terms list
        for term in record['terms']:
            t, created = Term.objects.get_or_create(name=term, language=self.source_language)
            terms.append(t)
            logger.debug("term : {}\n created : {} \n".format(term, created))
        # for each translation in a record, get or create in db, append to translations list
        for translation in record['translations']:
            t, created = Term.objects.get_or_create(name=translation, language=self.target_language)
            logger.debug("translation : {}\n created : {} \n".format(translation, created))
            translations.append(t)
        # for each domain in a record
        for domain in record['domain']:
            dom, created = Domain.objects.get_or_create(name=domain)
            print(dom, domain, type(domain))
            logger.debug("domain: {}\n created : {}".format(domain, created))
            domains.append(dom)

        return terms, translations, domains


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
                                                                        self.search.website)
