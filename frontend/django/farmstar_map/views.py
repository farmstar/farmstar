from django.http import HttpResponse
from django.http import HttpRequest
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http.response import StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
import json
import os

def livegeojson(request):
    if request.is_ajax():
        message = StreamingHttpResponse(staticfiles_storage.open('live.geojson'), content_type="application/json")
        return message
    else:
        message = StreamingHttpResponse(staticfiles_storage.open('live.geojson'), content_type="application/json")
        return message        

