from django.db import models
from django.conf import settings

from .utils import code_generator, create_shortcode
from .validators import validate_com_url

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class KirrModelManagar(models.Manager):
	def all(self, *args, **kwargs):
		queryset = super(KirrModelManagar, self).all(*args, **kwargs)
		qs = queryset.filter(active=True)
		return qs

	def refresh_shortcodes(self, items=None):
		qs = KirrURL.objects.filter(id__gte=1)
		if items is not None and isinstance(items, int):
			qs = qs.order_by('-id')[:items]
		new_codes = 0
		for q in qs:
			q.shortcode = str(create_shortcode(q))
			print(q.id, q.shortcode)
			q.save()
			new_codes += 1
		return f"New codes made: {new_codes}"


class KirrURL(models.Model):
	url = models.URLField(max_length=220, validators=[validate_com_url])
	shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	objects = KirrModelManagar()

	def __str__(self):
		return str(self.url)

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == '':
			self.shortcode = str(create_shortcode(self))
		super(KirrURL, self).save(*args, **kwargs)
