from django.db import models

from shortener.models import KirrURL

class ClickAnalysisManager(models.Manager):
	def click_analyse(self, instance):
		if isinstance(KirrURL, instance):
			obj, created = self.get_or_create(kirr_url=instance)
			obj.count += 1
			obj.save()
			return obj.count
		return None


class ClickAnalysis(models.Model):
	kirr_url = models.OneToOneField(KirrURL, on_delete=models.CASCADE)
	count = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{count}"

	objects = ClickAnalysisManager()
