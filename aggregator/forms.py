from django import forms
from .models import Language, Website


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class SearchForm(forms.Form):
    """
	translations,target_language,source_language,website,domain,terms,last_updated
	ordinateur,fr,en,iate,Pharmaceutical industry,computer,"[datetime.date(2016, 11, 18)]"
	"""

    keywords = forms.CharField(label='Search terms', max_length=100)
    source_language = forms.ModelChoiceField(Language.objects.all(), label="From", empty_label="Source language")
    target_language = forms.ModelChoiceField(Language.objects.all(), label="To", empty_label="Target language")
    websites = forms.ModelMultipleChoiceField(Website.objects.all(), label="", widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))

