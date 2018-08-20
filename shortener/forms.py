from django import forms
from django.core.validators import URLValidator

class ShortenURLForm(forms.Form):
	url = forms.URLField()
