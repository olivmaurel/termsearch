import logging
import os

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic.list import ListView
# Get an instance of a logger
from jinja2 import Environment, FileSystemLoader
from termsearch.settings import JINJA2_DIR
from itertools import chain

from .forms import SearchForm
from .models import Website, Language

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

def home_page(request):

    template = loader.get_template('aggregator/index.html')
    return HttpResponse(template.render())

def term_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            spiders_list = []

            for website in form.get_all_websites():
                # add the website.parse() to the chain

                spider = form.get_spider(website)
                print(form.get_all_websites())
                print(form.get_search_parameters())

                spiders_list.append(spider.parse())



            context = {'records': chain.from_iterable(spiders_list), 'form': SearchForm()}
            context.update(locals())

            return stream_http_with_jinja2_template('aggregator/search_results.html', context)

    else: # method='GET' or form is not valid
        form = SearchForm()
        return render(request, 'aggregator/search_home.html', locals())


def stream_http_with_jinja2_template(template, context):

    import termsearch.jinja2 as localj2
    j2_env = localj2.environment(loader=FileSystemLoader(JINJA2_DIR), trim_blocks=True)

    return StreamingHttpResponse(j2_env.get_template(template).generate(context))

class WebsiteListView(ListView):

    model = Website

    def get_context_data(self, **kwargs):
        context = super(WebsiteListView, self).get_context_data(**kwargs)
        return context