import random

from django.db import models

def code_generator(size=6, chars='qwertyuioplkjhgfdsazxcvbnm'):
	return ''.join(random.choice(chars) for _ in range(size))


class KirrURL(models.Model):
	url = models.URLField(max_length=220)
	shortcode = models.URLField(max_length=15, unique=True)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.url)

	def save(self, *args, **kwargs):
		print('saving this custom method')
		self.shortcode = code_generator()
		super(KirrURL, self).save(*args, **kwargs)
