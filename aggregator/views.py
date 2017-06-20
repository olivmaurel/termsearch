import logging
import os
from django.shortcuts import render
from django.views.generic.list import ListView
# Get an instance of a logger
from termsearch.settings.base import BASE_DIR
from termsearch.jinja2utils import stream_http_with_jinja2_template

from .forms import SearchForm
from .models import Website


logger = logging.getLogger(__name__)

def home_page(request):

    return render(request, 'aggregator/index.html', locals())

def term_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():

            websites = form.get_all_websites()
            records = form.get_records(websites)

            return stream_http_with_jinja2_template(request, 'aggregator/search_results.html', locals())

    else: # method='GET' or form is not valid
        form = SearchForm()
        logger.warning(locals())
        return render(request, 'aggregator/search_home.html', locals())


def about(request):
    about_md = get_md('about.md')
    return render(request, 'aggregator/about.html', locals())

def contact(request):
    contact_md = get_md('contact.md')
    return render(request, 'aggregator/contact.html', locals())


def get_md(filename):

    filepath = os.path.join(BASE_DIR, 'static/aggregator/md/{}'.format(filename))

    with open(filepath, 'r') as f:
        return f.read()

class WebsiteListView(ListView):

    model = Website

    def get_context_data(self, **kwargs):
        context = super(WebsiteListView, self).get_context_data(**kwargs)
        return context