from django.db import models

from .utils import code_generator, create_shortcode

class KirrModelManagar(models.Manager):
	def all(self, *args, **kwargs):
		queryset = super(KirrModelManagar, self).all(*args, **kwargs)
		qs = queryset.filter(active=True)
		return qs

	def refresh_shortcodes(self, items):
		print(items)
		qs = KirrURL.objects.filter(id__gte=1)
		new_codes = 0
		for q in qs:
			q.shortcode = 'http://' + str(create_shortcode(q)) + '.co'
			print(q.shortcode)
			q.save()
			new_codes += 1
		return f"New codes made: {new_codes}"


class KirrURL(models.Model):
	url = models.URLField(max_length=220)
	shortcode = models.URLField(max_length=15, unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	objects = KirrModelManagar()

	def __str__(self):
		return str(self.url)

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == '':
			self.shortcode = 'http://' + str(create_shortcode(self)) + '.co'
		super(KirrURL, self).save(*args, **kwargs)
