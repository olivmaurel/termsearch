## jinja tester
import os
from itertools import chain

from django.http import StreamingHttpResponse
from jinja2 import Environment, FileSystemLoader

from aggregator.models import Language
from aggregator.spiders import *

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

search_parameters = {'keywords': 'computer',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}
iate = IateSpider(**search_parameters)
termium = TermiumSpider(**search_parameters)
proz = ProzSpider(**search_parameters)



results = chain(iate.parse(), termium.parse(), proz.parse())




#######################

from aggregator.models import Language
from aggregator.forms import SearchForm

searchform = SearchForm()
searchform.keywords = "computer"
searchform.source_language = Language.objects.get(code2d='en')
searchform.target_language = Language.objects.get(code2d='fr')
searchform.is_bound = True


#############################
# copypaste this in the shell for testing proz

from aggregator.models import Language
from aggregator.spiders import *

search_parameters = {'keywords': 'tennis',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

proz = ProzSpider(**search_parameters)

print ([res for res in proz.parse()])

# if parse() returns an error, do it again step by step

response = requests.post(proz.url, data=proz.formdata)
json_response = json.loads(response.text)['html']
html_tree = html.fromstring(json_response)
page_results = html_tree.xpath('//tbody[@class=\'search_result_body\']/tr/td[4]')


########################





####
def mytest():

    context = {'my_list': [1, 2, 3, 4, 5], 'my_string': 'goddamit', 'records': results}
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    loader = FileSystemLoader(filename)
    template = env.get_template(loader)
    stream = template.generate(context)
    return StreamingHttpResponse(stream)

