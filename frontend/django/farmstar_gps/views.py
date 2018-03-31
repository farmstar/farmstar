from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http.response import StreamingHttpResponse
from django.views.decorators.http import require_http_methods
import subprocess
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .import forms
from farmstar_gps.models import STATUS
from django.http import JsonResponse

def GPSon(request):
    gps.GPSstatus(request)
    status = STATUS.objects.latest('id').STATUS
    return JsonResponse({'gps_status': status})

def GPSoff(request):
    gps.GPSstatus(request)
    status = STATUS.objects.latest('id').STATUS
    return JsonResponse({'gps_status': status})
