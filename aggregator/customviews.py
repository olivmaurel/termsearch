import io
import logging
import time
import os
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render

from jinja2 import Environment, FileSystemLoader
from itertools import chain
from .forms import SearchForm
from .models import Search, Language
from .scraper.spiders import IateSpider, TermiumSpider, ProzSpider
from .views import stream_http_with_jinja2_template
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Get an instance of a logger
logger = logging.getLogger(__name__)


def normal_httpresponse(request): # todo remove after testing
    import scrapydo
    from aggregator.scraper.scrapy_spiders import IateSpider


    scrapydo.setup()

    search_parameters = {'keywords': 'computer',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    return HttpResponse(scrapydo.run_spider(IateSpider(**search_parameters), yield_items=True, capture_items=False,
                            **search_parameters))

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
    # use the correct path for the jinja2 templates : termsearch/jinja2/aggregator
    # 'jinja2' should replace 'template' as the top folder
    # use the most basic context
    results = slow_response_for_testing_streaming(5)
    context = {'my_list': [1, 2, 3, 4, 5], 'my_string': 'goddamit', 'records': results}
    # render it in a basic crude template
    return stream_http_with_jinja2_template('fixit/streamer.html', context)



def use_scrapy_with_downloader(stream):
    # dfd = spider.crawler.engine.download(request, spider)
    import scrapy
    from aggregator.scraper.scrapy_spiders import IateSpider
    from aggregator.models import Language

    search_parameters = {'keywords': 'boilerplate',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    spider = IateSpider (**search_parameters)

    request = scrapy.Request(url=spider.remoteurl)

    response = spider.crawler.engine.download(request, spider)

    return IateSpider.parse(response)



def streaming_spider(stream):

    import scrapydo
    from scrapy import signals
    from aggregator.scraper.scrapy_spiders import IateSpider
    from aggregator.models import Language

    scrapydo.setup()

    def item_passed(item):
        stream._set_streaming_content(item)

    def spider_closed():
        stream.close()

    def setup_crawler(crawler):
        crawler.signals.connect(signals.item_passed, item_passed)
        crawler.signals.connect(signals.spider_closed, spider_closed)

    search_parameters = {'keywords': 'boilerplate',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    scrapydo.run_spider(IateSpider(**search_parameters), capture_items=False, **search_parameters)


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
