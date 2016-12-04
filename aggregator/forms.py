from django import forms
from .models import Language, Website


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class SearchForm(forms.Form):
	"""
	translations,targetLanguage,sourceLanguage,website,domain,terms,last_updated
ordinateur,fr,en,iate,Pharmaceutical industry,computer,"[datetime.date(2016, 11, 18)]"
	"""

	keywords = forms.CharField(label='Search terms', max_length=100)
	sourceLanguage = forms.ModelChoiceField(Language.objects.all(), label="From", empty_label="Source language")
	targetLanguage = forms.ModelChoiceField(Language.objects.all(), label="To", empty_label="Target language")
	websites = forms.ModelMultipleChoiceField(Website.objects.all(), label="", widget=forms.CheckboxSelectMultiple)

	def process_request(self):
		#TODO
		pass