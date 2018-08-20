from django import forms

class ShortenURLForm(forms.Form):
	url = forms.URLField()

	def clean(self):
		cleaned_data = super().clean()
		url = cleaned_data['url']
		print(url)

	def cleaned_url(self):
		url = self.cleaned_data['url']
		print(url)
		return url
