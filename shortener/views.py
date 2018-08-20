from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from .models import KirrURL

class HomeView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'shortener/home.html', {})

	def post(self, request, *args, **kwargs):
		return render(request, 'shortener/home.html', {})


class KirrRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		object = get_object_or_404(KirrURL, shortcode=shortcode)
		obj_url = object.url
		return HttpResponseRedirect(obj_url)
