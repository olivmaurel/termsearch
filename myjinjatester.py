## jinja tester
from aggregator.models import Language
from aggregator.scraper.spiders import *
from itertools import chain
from django.http import StreamingHttpResponse
from jinja2 import Environment, FileSystemLoader, Template

import os

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

search_parameters = {'keywords': 'computer',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}
iate = IateSpider(**search_parameters)
termium = TermiumSpider(**search_parameters)
proz = ProzSpider(**search_parameters)



results = chain(proz.parse(), termium.parse(), proz.parse())

context = {'my_list':[1,2,3,4,5], 'my_string':'goddamit', 'records': results}

env = Environment()

localdir = '/home/olivier/pythonstuff/projects/termsearch/aggregator/templates/jinja2/'

filename = 'streamer.html'

#######################

from aggregator.models import Language
from aggregator.scraper.spiders import *
from itertools import chain
from aggregator.forms import SearchForm

searchform = SearchForm()
searchform.keywords = "computer"
searchform.source_language = Language.objects.get(code2d='en')
searchform.target_language = Language.objects.get(code2d='fr')
searchform.is_bound = True




########################





####
def mytest():

    context = {'my_list': [1, 2, 3, 4, 5], 'my_string': 'goddamit', 'records': results}
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    loader = FileSystemLoader(filename)
    template = env.get_template(loader)
    stream = template.generate(context)
    return StreamingHttpResponse(stream)

