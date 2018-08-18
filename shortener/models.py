from django.db import models

from .utils import code_generator, create_shortcode

class KirrURL(models.Model):
	url = models.URLField(max_length=220)
	shortcode = models.URLField(max_length=15, unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return str(self.url)

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == '':
			self.shortcode = 'http://' + str(create_shortcode(self)) + '.co'
		super(KirrURL, self).save(*args, **kwargs)
