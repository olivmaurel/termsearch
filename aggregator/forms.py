import logging

from django import forms
from django.db.models import Q

from .models import Language, Website

# Get an instance of a logger
logger = logging.getLogger(__name__)


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class SearchForm(forms.Form):
    """
	translations,target_language,source_language,website,domain,terms,last_updated
	ordinateur,fr,en,iate,Pharmaceutical industry,computer,"[datetime.date(2016, 11, 18)]"
	"""
    keywords_charfield_attrs = forms.TextInput(attrs={'size':80,
                                                      'placeholder':"Search for term"})
    keywords = forms.CharField(max_length=100,
                               widget=keywords_charfield_attrs
                               )
    source_language = forms.ModelChoiceField(Language.objects.all().order_by('code2d'),
                                             label="From",
                                             label_suffix=": ",
                                             empty_label="Source language"
                                             )
    target_language = forms.ModelChoiceField(Language.objects.all().order_by('code2d'),
                                             label="To",
                                             label_suffix=": ",
                                             empty_label="Target language"
                                             )
    def get_all_websites(self):
        '''
        Check first that the form is valid (should never be called if the form is not valid)
        returns an empty Queryset if the form is not valid

        In a normal situation, returns the merged list of all the websites using the language pair selected

        Example : Termium is EN/FR/ES/PT only, don't include it when searching in DE, IT etc...

        '''
        if self.is_valid():
            q_source_language = Q(languages=self.cleaned_data['source_language'])
            q_target_language = Q(languages=self.cleaned_data['target_language'])
            website_list = Website.objects.filter(q_source_language).filter(q_target_language).distinct().order_by('id')
            return website_list
        else:
            return Website.objects.none()