from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

from .models import KirrURL

def kirr_redirect_view(request, shortcode=None, *args, **kwargs):
	object = get_object_or_404(KirrURL, shortcode=shortcode)
	obj_url = object.url
	return HttpResponse(f'<h1>Kirr Url Shortener {obj_url}</h1>')


class KirrRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		object = get_object_or_404(KirrURL, shortcode=shortcode)
		obj_url = object.url
		return HttpResponse(f"<h1>Kirr Url Shortener Again {obj_url}</h1>")
