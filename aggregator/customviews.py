import io
import logging
import os
import time
from itertools import chain

from django.http import StreamingHttpResponse
from django.shortcuts import render

from aggregator.spiders import IateSpider, TermiumSpider, ProzSpider
from .forms import SearchForm
from .models import Search, Language
from .views import stream_http_with_jinja2_template

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Get an instance of a logger
logger = logging.getLogger(__name__)


def simplestreamer(request):

    from itertools import chain

    search_parameters = {'keywords': 'computer',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    iate = IateSpider(**search_parameters)
    termium = TermiumSpider(**search_parameters)
    proz = ProzSpider(**search_parameters)

    results = chain(iate.parse(), termium.parse(), proz.parse())

    return StreamingHttpResponse(results)

def jinja_tester(request):

    search_parameters = {'keywords': 'lectin',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    iate = IateSpider(**search_parameters)
    termium = TermiumSpider(**search_parameters)
    proz = ProzSpider(**search_parameters)

    results = chain(iate.parse(), termium.parse(), proz.parse())

    context = {'my_list':[1,2,3,4,5], 'my_string':'goddamit', 'records': results}

    return stream_http_with_jinja2_template('jinja2/streamer.html', context)
    # return render(request, 'jinja2/streamer.html', context)


def fix_the_template_mess(request):

    # todo get the static directory right
    # use the correct path for the jinja2 templates
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
