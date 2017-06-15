import logging
import os
from django.shortcuts import render
from django.views.generic.list import ListView
# Get an instance of a logger
from termsearch.settings import BASE_DIR

logger = logging.getLogger(__name__)

def index(request):

    return render(request, 'news/index.html', locals())

def releases(request):
    releases_md = get_md('releases.md')
    return render(request, 'news/releases.html', locals())

def todopage(request):

    todopage_md = get_md('todopage.md')
    return render(request, 'news/todopage.html', locals())


def get_md(filename):

    filepath = os.path.join(BASE_DIR, 'static/news/md/{}'.format(filename))

    with open(filepath, 'r') as f:
        return f.read()