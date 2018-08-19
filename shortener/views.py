from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models import KirrURL

def kirr_redirect_view(request, shortcode=None, *args, **kwargs):
	object = KirrURL.objects.get(shortcode=shortcode)
	return HttpResponse(f'<h1>Kirr Url Shortener {object.url}</h1>')


class KirrRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		object = KirrURL.objects.get(shortcode=shortcode)
		return HttpResponse(f"<h1>Kirr Url Shortener Again {object.url}</h1>")
