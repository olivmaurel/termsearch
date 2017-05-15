import logging

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic.list import ListView
# Get an instance of a logger

from termsearch import local_jinja2

from .forms import SearchForm
from .models import Website


logger = logging.getLogger(__name__)

def home_page(request):

    template = loader.get_template('aggregator/index.html')
    return HttpResponse(template.render())


def term_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():

            records = form.get_records()

            return stream_http_with_jinja2_template(request, 'aggregator/search_results.html', locals())

    else: # method='GET' or form is not valid
        form = SearchForm()
        logger.warning(locals())
        return render(request, 'aggregator/search_home.html', locals())




def stream_http_with_jinja2_template(request, template, context):

    j2_env = local_jinja2.environment_with_loader()

    if request is not None:
        from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
        context['request'] = request
        context['csrf_input'] = csrf_input_lazy(request)
        context['csrf_token'] = csrf_token_lazy(request)

    return StreamingHttpResponse(j2_env.get_template(template).generate(context))

class WebsiteListView(ListView):

    model = Website

    def get_context_data(self, **kwargs):
        context = super(WebsiteListView, self).get_context_data(**kwargs)
        return context