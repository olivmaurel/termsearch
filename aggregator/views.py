from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from .forms import SearchForm, NameForm
from django.views.generic.edit import FormView
from .models import Domain

from .models import Search

def index(request):
    template = loader.get_template('aggregator/index.html')
    return HttpResponse(template.render())


def term_search(request):
    if request.method == 'POST':
        
        form = SearchForm(request.POST)
        res = ""

        if form.is_valid():
            for w in form.cleaned_data['websites']:

                s = Search()
                s.keywords = form.cleaned_data['keywords']
                s.sourceLanguage = form.cleaned_data['sourceLanguage']
                s.targetLanguage = form.cleaned_data['targetLanguage']
                s.website = w
                s.domain = Domain(name="no domain yet")
                s.results = {"res": "no results yet"}
                res += "{}<br>".format(s)
            #return HttpResponseRedirect('results', keywords)
            return HttpResponse("You searched for :<br> {}".format(res))
    else:
        form = SearchForm()
    return render(request, 'aggregator/term_search.html', locals())

 
def crawler_results(request):
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.project import get_project_settings
    # I want to call the scrapy spider here.
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE","whereyourscrapysettingsare")
    crawler_settings = get_project_settings()
    crawler = CrawlerRunner(crawler_settings)
    crawler.crawl(yourspider, key=key)

    return HttpResponse("HO HO HO")    