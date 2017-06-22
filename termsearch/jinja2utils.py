from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment, FileSystemLoader
from termsearch.settings.base import JINJA2_DIR
from django.http import StreamingHttpResponse
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
import os
from termsearch.settings.base import BASE_DIR


def markdown(md):
    """
    Markdown to HTML conversion.
    """
    import bleach
    from markdown import markdown
    allowed_tags = ['a', 'abbr', 'acronym', 'b',
                    'blockquote', 'code', 'em',
                    'i', 'li', 'ol', 'pre', 'strong',
                    'ul', 'h1', 'h2', 'h3', 'p', 'br', 'ins', 'del']
    return bleach.linkify(bleach.clean(
        markdown(md, output_format='html', extensions=['nl2br', 'del_ins']),
        tags=allowed_tags, strip=True))



def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.filters['markdown'] = markdown
    return env



def environment_with_loader():

    return environment(loader=FileSystemLoader(JINJA2_DIR), trim_blocks=True)


def stream_http_with_jinja2_template(request, template, context):

    j2_env = environment_with_loader()

    if request is not None:
        context['csrf_input'] = csrf_input_lazy(request)
        context['csrf_token'] = csrf_token_lazy(request)

    return StreamingHttpResponse(j2_env.get_template(template).generate(context))

def get_md(filename):

    filepath = os.path.join(BASE_DIR, filename)

    with open(filepath, 'r') as f:
        return f.read()

