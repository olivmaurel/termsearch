import os
from jinja2 import Environment, FileSystemLoader

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = "/aggregator/templates/"
def print_html_doc():
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print (line for line in j2_env.get_template('aggregator/templates/jinja2/basehtml').generate(
           title='Hellow Gist from GutHub'))



def generate_fromstream(template, context):


    path = THIS_DIR + TEMPLATE_FOLDER

    j2_env = Environment(loader=FileSystemLoader(path),
                         trim_blocks=True)

    return [html for html in j2_env.get_template(template).generate(context)]


if __name__ == '__main__':

    template = 'jinja2/streamer.html'

    path = '/home/olivier/pythonstuff/projects/termsearch/aggregator/templates/'

    context = {'my_list': [1, 2, 3, 4, 5], 'my_string': 'goddamit', 'records': 'a'}

    print (generate_fromstream(template, context))

