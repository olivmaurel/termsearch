from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment, FileSystemLoader
from termsearch.settings import JINJA2_DIR
from django.http import StreamingHttpResponse
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env

def environment_with_loader():

    return environment(loader=FileSystemLoader(JINJA2_DIR), trim_blocks=True)


def stream_http_with_jinja2_template(request, template, context):

    j2_env = environment_with_loader()

    if request is not None:
        context['csrf_input'] = csrf_input_lazy(request)
        context['csrf_token'] = csrf_token_lazy(request)

    return StreamingHttpResponse(j2_env.get_template(template).generate(context))