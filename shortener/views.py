from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from .models import KirrURL
from .forms import ShortenURLForm

class HomeView(View):
	def get(self, request, *args, **kwargs):
		form = ShortenURLForm()
		context = {
			'form': form
		}
		return render(request, 'shortener/home.html', context)

	def post(self, request, *args, **kwargs):
		form = ShortenURLForm(request.POST)
		context = {
			'form': form
		}
		template = "shortener/home.html"
		if form.is_valid():
			new_url = form.cleaned_data.get('url')
			obj, created = KirrURL.objects.get_or_create(url=new_url)
			context = {
				'obj': obj,
				'created': created
			}
			if created:
				template = 'shortener/success.html'
			else:
				template = 'shortener/already-exists.html'
		return render(request, template, context)


class KirrRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		object = get_object_or_404(KirrURL, shortcode=shortcode)
		obj_url = object.url
		return HttpResponseRedirect(obj_url)
