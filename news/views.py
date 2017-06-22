import logging
from django.shortcuts import render
# Get an instance of a logger
from termsearch.jinja2utils import get_md

logger = logging.getLogger(__name__)

def index(request):

    return render(request, 'news/index.html', locals())

def releases(request):
    releases_md = get_md('static/news/md/releases.md')
    return render(request, 'news/releases.html', locals())

def todopage(request):

    todopage_md = get_md('static/news/md/todopage.md')
    return render(request, 'news/todopage.html', locals())
