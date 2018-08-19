from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

def kirr_redirect_view(request, *args, **kwargs):
	return HttpResponse('<h1>Kirr Url Shortener</h1>')


class KirrRedirectView(View):
	def get(self, request, *args, **kwargs):
		return HttpResponse("<h1>Kirr Url Shortener Again</h1>")
