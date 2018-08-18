import random
import string

from django.db import models

def code_generator(size=5, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
	return ''.join(random.choice(chars) for _ in range(size))


class KirrURL(models.Model):
	url = models.URLField(max_length=220)
	shortcode = models.URLField(max_length=15, unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.url)

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == '':
			self.shortcode = 'http://' + str(code_generator()) + '.co'
		super(KirrURL, self).save(*args, **kwargs)
