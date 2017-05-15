from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment, FileSystemLoader
from termsearch.settings import JINJA2_DIR


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env

def environment_with_loader():

    return environment(loader=FileSystemLoader(JINJA2_DIR), trim_blocks=True)