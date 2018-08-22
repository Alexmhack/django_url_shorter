from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .validators import validate_com_url

class ShortenURLForm(forms.Form):
	url = forms.URLField()
