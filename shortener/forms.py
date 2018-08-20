from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_com_url(value):
	if 'com' not in value:
		raise ValidationError("Entered URL is not a valid .com url")
	return value


class ShortenURLForm(forms.Form):
	url = forms.URLField(validators=[validate_com_url])
