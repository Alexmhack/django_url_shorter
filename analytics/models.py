from django.db import models

from shortener.models import KirrURL

class ClickAnalysis(models.Model):
	kirr_url = models.OneToOneField(KirrURL)
	count = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{count}"
