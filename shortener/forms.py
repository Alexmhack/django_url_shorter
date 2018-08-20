from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_url(value):
	url_validator = URLValidator()
	try:
		url_validator(value)
	except Exception as e:
		raise ValidationError(e)
	return value


class ShortenURLForm(forms.Form):
	url = forms.URLField(validators=[validate_url])
