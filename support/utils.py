# utils.py
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest

def build_absolute_url(request: HttpRequest, view_name: str, *args, **kwargs) -> str:
    protocol = 'https' if request.is_secure() else 'http'
    domain = get_current_site(request).domain
    return f"{protocol}://{domain}{reverse(view_name, args=args, kwargs=kwargs)}"
