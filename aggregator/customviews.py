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
from .views import stream_http_with_jinja2_template

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

def jinja_tester(request):

    search_parameters = get_test_search_parameters()

    termium = TermiumSpider(**search_parameters)
    proz = ProzSpider(**search_parameters)

    spiders_list = [proz.parse()]

    records = get_records(spiders_list)

    context = {'my_list':[1,2,3,4,5], 'my_string': locals(), 'records': records, 'form':SearchForm()}

    return stream_http_with_jinja2_template('aggregator/search_results.html', context)



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

def fix_the_template_mess(request):

    # todo get the static directory right
    # use the correct path for the jinja2 templates
    # 'jinja2' should replace 'template' as the top folder
    # use the most basic context
    results = slow_response_for_testing_streaming(5)
    context = {'my_list': [1, 2, 3, 4, 5], 'my_string': 'goddamit', 'records': results}
    # render it in a basic crude template
    return stream_http_with_jinja2_template('fixit/streamer.html', context)


def streaming_io():

    stream = io.StringIO("Let's start streaming...")
    for i in range(10):
        # time.sleep(1)
        stream.write("{}<br/>".format(i))

    return stream.read()


def slow_response_for_testing_streaming(delay):

    for i in range(delay):
        time.sleep(1)
        yield "Wew that's taking a while, hold on .... {}<br/>".format(delay)


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
