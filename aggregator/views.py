import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .forms import SearchForm
from .models import Search, Record

# Get an instance of a logger
logger = logging.getLogger(__name__)



def index(request):
    template = loader.get_template('aggregator/index.html')
    return HttpResponse(template.render())


def term_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            for website in form.cleaned_data['websites']:

                search, search_created = Search.objects.get_or_create(
                                        keywords=form.cleaned_data['keywords'],
                                        source_language = form.cleaned_data['source_language'],
                                        target_language = form.cleaned_data['target_language'],
                                        website = website,
                                        )
                search.domains.add(1) # todo implement manytomany domains
                logger.debug("{} \n New search:{}".format(search, search_created))

                if search_created:
                    # go scrape the results
                    queryset = scraper(search)
                else:
                    # take the results from the db
                    # all the records matching 'search' - foreign key
                    queryset = search.record_set.all()
            context = {
                    "queryset": queryset,
                    "form": form
                    }
            # return HttpResponse('Results found: {}<br>You searched for :<br> {} <br> {}'.format(len(results), search, results))
            return render(request, 'aggregator/term_search.html', context)
    else:
        form = SearchForm()
    return render(request, 'aggregator/term_search.html', locals())

def spider_results_as_django_records(search, spider):
    '''
    :param search: django.models.Search
    :param spider: scrapydo spider
    :return: a list of django.models.Record objects
    '''
    django_records = []

    # for each record in results
    for record in spider:
        # create a new django.models.Record, and add it to the list
        django_records.append(create_record(search, record))

    return django_records

def create_record(search, record):
        '''
        :param search: django.models.Search
        :param record: scrapy.items.Record
        :return: django.models.Record
        creates a new Record object using Record.objects.create()
        adds terms and translations as a list (Manytomany

        '''
        new_record = Record.objects.create(search=search)
        # list of Term objects (terms, translations, domains) to save in Record
        terms, translations, domains = search.get_or_create_manytomanys(record)
        new_record.terms.add(*terms)
        new_record.translations.add(*translations)
        new_record.domains.add(*domains)
        return record


def scraper(search):
    '''

    :param search: django.models.Search
    :return: a list of django.models.Record objects
    '''
    from .scraper.spiders.iate import IateSpider

    import scrapydo

    scrapydo.setup()

    logger.debug("Now sending HTTP request to get results from {}".format(search.website))
    search_parameters = {
        'keywords': search.keywords,
        'source_language': search.source_language,
        'target_language': search.target_language
    }
    logger.debug("Search_parameters : {}".format(search_parameters))


    spider = scrapydo.run_spider(IateSpider(**search_parameters), **search_parameters)
    # add each record to the db
    spider_results_as_django_records(search, spider)  # test


    # and return a Queryset of django.models.Record
    return search.record_set.all()

