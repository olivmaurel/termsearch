from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from .forms import SearchForm
from django.views.generic.edit import FormView

class SearchView(FormView):
    template_name = 'search.html'
    form_class = SearchForm
    success_url = '/thanks/'

    def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
        form.process_request()
        return super(ContactView, self).form_valid(form)

def index(request):
    template = loader.get_template('search/search.html')
    return HttpResponse(template.render())


def results(request, search_id):
    response = "You're looking at the results of search %s."
    return HttpResponse(response % question_id) 