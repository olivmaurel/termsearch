## jinja tester
from aggregator.models import Language
from aggregator.scraper.spiders import *
import requests
from itertools import chain
from django.http import HttpResponse, StreamingHttpResponse
import jinja2
from jinja2 import BaseLoader, TemplateNotFound

search_parameters = {'keywords': 'computer',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}
iate = IateSpider(**search_parameters)
termium = TermiumSpider(**search_parameters)
proz = ProzSpider(**search_parameters)



results = chain(proz.parse(), termium.parse(), proz.parse())

context = {'my_list':[1,2,3,4,5], 'my_string':'goddamit', 'records': results}

filename = 'jinja2/streamer.html'
env = jinja2.Environment()
template = jinja2.Template(filename)

rendered = template.render(**context)



####
def mytest():

    context = {'my_list': [1, 2, 3, 4, 5], 'my_string': 'goddamit', 'records': results}
    env = jinja2.Environment()
    loader = jinja2.FileSystemLoader(filename)
    template = env.get_template(loader)
    stream = template.generate(context)
    return StreamingHttpResponse(stream)