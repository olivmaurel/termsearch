from django import forms
from .models import Language, Website


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class SearchForm(forms.Form):
	"""
	translations,targetLanguage,sourceLanguage,website,domain,terms,last_updated
ordinateur,fr,en,iate,Pharmaceutical industry,computer,"[datetime.date(2016, 11, 18)]"
	"""

	keywords = forms.CharField(label='search_keywords', max_length=100)
	sourceLanguage = forms.ModelChoiceField(Language)
	targetLanguage = forms.ModelChoiceField(Language)
	website = forms.ModelChoiceField(Website)

	def proces_request(self):
		#TODO
		pass