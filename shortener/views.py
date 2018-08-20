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
		if form.is_valid():
			print(form.cleaned_data)
		return render(request, 'shortener/home.html', context)


class KirrRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		object = get_object_or_404(KirrURL, shortcode=shortcode)
		obj_url = object.url
		return HttpResponseRedirect(obj_url)
