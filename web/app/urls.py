from django.urls import path, re_path
from django.conf.urls.static import serve

from web.web import settings


urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve ,{'document_root': settings.STATIC_ROOT}), 
]

