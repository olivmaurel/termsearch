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
                logger.info("{} \n New search:{}".format(search, search_created))

                if search_created:
                    # go scrape the results
                    queryset = search.scraper()
                else:
                    # take the results from the db
                    # all the records matching 'search' - foreign key
                    queryset = search.record_set.all()
                    logger.info("record set : {}".format(search.record_set.all()))
            context = {
                    "queryset": queryset,
                    "form": form
                    }

            return render(request, 'aggregator/search_results.html', context)
    else:
        form = SearchForm()
        return render(request, 'aggregator/term_search.html', locals())
