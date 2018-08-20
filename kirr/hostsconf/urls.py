from django.urls import re_path

from .views import wildcard_redirect

urlpatterns = [
	re_path(r'^(?P<path>.*)', wildcard_redirect, name='wildcard-redirect'),
]
