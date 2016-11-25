from django.contrib.postgres.fields import JSONField
from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=30)
    code3d = models.CharField(max_length=3)
    code2d = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Website(models.Model):
    name = models.CharField(max_length=50)
    homepage = models.URLField()
    search_url = models.URLField()
    languages = models.ManyToManyField(Language)

    def getLanguages(self):
        res = []
        for l in self.languages.all():
             res.append(l)
        return res     

    def __str__(self):
        return self.name

class Domain (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Term(models.Model):
    name = models.CharField(max_length=200)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

class Record(models.Model):
    terms = models.ManyToManyField(Term, related_name="terms")
    translations = models.ManyToManyField(Term, related_name="translations")
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    lastUpdate = models.DateTimeField('last update')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

class Search(models.Model):
    keyword = models.CharField(max_length=100)
    date = models.DateTimeField()
    results = JSONField()