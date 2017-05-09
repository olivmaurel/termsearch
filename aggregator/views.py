import logging
import os

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic.list import ListView

from .forms import SearchForm
from .models import Search, Website
from .scraper.spiders import IateSpider, TermiumSpider, ProzSpider
from aggregator.models import Language
# Get an instance of a logger
from itertools import chain
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

def home_page(request):

    template = loader.get_template('aggregator/index.html')
    return HttpResponse(template.render())


def scrapy_term_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            search_queryset = Search.objects.none()

            for website in form.get_all_websites():

                search, search_not_in_db = Search.objects.get_or_create(
                                        keywords=form.cleaned_data['keywords'],
                                        source_language = form.cleaned_data['source_language'],
                                        target_language = form.cleaned_data['target_language'],
                                        website = website,
                                        )
                search.domains.add(1) # todo implement manytomany domains
                logger.info("{} \n New search:{}".format(search, search_not_in_db))

                if search_not_in_db:
                    scrapy_results = search.get_records_from_scrapy()
                    search.save_results_in_db(scrapy_results)

                search_queryset = search_queryset | search.record_set.all()
                logger.info("record set : {}".format(search.record_set.all()))

            context = {
                "queryset": search_queryset,
                "form": form
                }

            return render(request, 'aggregator/search_results.html', context)
    else:
        form = SearchForm()
        return render(request, 'aggregator/search_home.html', locals())


def term_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            # results = chain()
            # for each website corresponding to the language pair
            print('a')
            # for website in form.get_all_websites():
                # add the website.parse() to the chain

                #spider = form.get_spider(website)
                # print(form.get_all_websites())
                # print(form.get_search_parameters())

            context = {'results': ['a', 'b', 'c']}

            return stream_http_with_jinja2_template('jinja2/search_results.html', context)

    else: # method='GET' or form is not valid
        form = SearchForm()
        return render(request, 'aggregator/search_home.html', locals())



def stream_http_with_jinja2_template(template, context):

    path = THIS_DIR + '/templates/'
    j2_env = Environment(loader=FileSystemLoader(path), trim_blocks=True)

    return StreamingHttpResponse(j2_env.get_template(template).generate(context))

class WebsiteListView(ListView):

    model = Website

    def get_context_data(self, **kwargs):
        context = super(WebsiteListView, self).get_context_data(**kwargs)
        return context