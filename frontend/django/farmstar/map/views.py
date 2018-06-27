from django.shortcuts import render

from django.http import HttpResponse

from django.template.response import TemplateResponse

'''
def index(request):
    return HttpResponse("Hello fuckers you are at the farmstar index.")

'''

def index(request):
    return TemplateResponse(request, 'map.html')
