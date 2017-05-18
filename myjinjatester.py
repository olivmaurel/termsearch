## jinja tester
import os
from itertools import chain

from django.http import StreamingHttpResponse
from jinja2 import Environment, FileSystemLoader

from aggregator.models import Language
from aggregator.spiders import *


#############################
# copypaste this in the shell for testing proz

from aggregator.models import Language
from aggregator.spiders import *

search_parameters = {'keywords': 'tennis',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

proz = ProzSpider(**search_parameters)

# if parse() returns an error, do it again step by step

response = requests.post(proz.url, data=proz.formdata)
json_response = json.loads(response.text)['html']
html_tree = html.fromstring(json_response)
page_results = html_tree.xpath('//tbody[@class=\'search_result_body\']/tr/td[4]')


########################



