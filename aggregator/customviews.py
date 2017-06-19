import io
import logging
import os
import time
from itertools import chain

from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import StreamingHttpResponse
from django.shortcuts import render

from aggregator.spiders import IateSpider, TermiumSpider, ProzSpider
from .forms import SearchForm
from .models import Search, Language
from termsearch.jinja2utils import stream_http_with_jinja2_template

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_records(list_of_generators):

    records = chain.from_iterable(list_of_generators)
    return records

def get_test_search_parameters(term):

    search_parameters = {'keywords': term,
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    return search_parameters

def search_with_timer(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            websites = form.get_all_websites()
            records = form.get_records(websites)

            return stream_http_with_jinja2_template(request, 'aggregator/search_results.html', locals())

    else:  # method='GET' or form is not valid
        form = SearchForm()
        logger.warning(locals())
        return render(request, 'aggregator/search_home.html', locals())



def proz_spider_tester(request, term):
    search_parameters = get_test_search_parameters(term)
    spider = ProzSpider(**search_parameters)

    return StreamingHttpResponse(spider.parse())

def iate_spider_tester(request, term):
    search_parameters = get_test_search_parameters(term)
    spider = IateSpider(**search_parameters)

    return StreamingHttpResponse(spider.parse())

def termium_spider_tester(request, term):
    search_parameters = get_test_search_parameters(term)
    spider = TermiumSpider(**search_parameters)

    return StreamingHttpResponse(spider.parse())


def test_httpresponse(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():

            records = form.get_records()

            return render(request, 'aggregator/search_results.html', locals())

    else: # method='GET' or form is not valid
        form = SearchForm()
        logger.warning(locals())
        return render(request, 'aggregator/search_home.html', locals())


def test_jinja_generate(request):

    results = slow_response_for_testing_streaming(5)
    context = {'my_list': [1, 2, 3, 4, 5], 'my_string': 'This is a string.', 'results': results, 'request': request}
    # render it in a basic crude template
    return stream_http_with_jinja2_template(request, 'aggregator/test_template.html', context)


def safemode_search(request):
    from itertools import chain
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            search_parameters = form.get_search_parameters()

            proz = ProzSpider(**search_parameters)
            iate = IateSpider(**search_parameters)

            # faking long request with delays inbetween parsing jobs
            # records = chain(form.delay(), proz.parse(), form.delay(), iate.parse(), form.delay())
            records = chain(proz.parse(), iate.parse())

            return stream_http_with_jinja2_template(request,'aggregator/safemode_search.html', locals())
    else:
        form = SearchForm()
        return render(request, 'aggregator/safemode_search.html', locals())



def django_streamingthttp_tester(request):

    return StreamingHttpResponse(slow_response_for_testing_streaming(10))

def slow_response_for_testing_streaming(delay):

    for i in range(delay):
        time.sleep(1)
        yield "Wew that's taking a while, hold on .... {}<br/>".format(delay-i  )


def mytestsearch(request):

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
                    page_results = search.get_records()
                    search.save_results_in_db(page_results)

                search_queryset = search_queryset | search.record_set.all()

            context = {
                "queryset": search_queryset,
                "form": form
                }

            return render(request, 'aggregator/search_results.html', context)
    else:
        form = SearchForm()
        return render(request, 'aggregator/search_home.html', locals())
