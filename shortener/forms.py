from django import forms
from django.core.validators import URLValidator

class ShortenURLForm(forms.Form):
	url = forms.URLField()

	def clean(self):
		cleaned_data = super().clean()

	def cleaned_url(self):
		url = self.cleaned_data['url']
		print(url)
		url_validator = URLValidator()
		try:
			url_validator(url)
		except Exception as e:
			raise forms.ValidationError("Invalid URL entered", e)
		return url
