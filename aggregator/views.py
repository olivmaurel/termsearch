import logging

from django.shortcuts import render
from django.views.generic.list import ListView
# Get an instance of a logger

from termsearch.local_jinja2 import stream_http_with_jinja2_template

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
    # todo the about page
    return render(request, 'aggregator/about.html', locals())

def contact(request):
    # todo the contact page
    print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])
    return render(request, 'aggregator/contact.html', locals())


class WebsiteListView(ListView):

    model = Website

    def get_context_data(self, **kwargs):
        context = super(WebsiteListView, self).get_context_data(**kwargs)
        return context