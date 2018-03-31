"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from . import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='clock_index.html'), name='home'),
    url(r'^flip', TemplateView.as_view(template_name='clock_flip.html'), name='flip'),
    url(r'^simple', TemplateView.as_view(template_name='clock_simple.html'), name='simple'),
    url(r'^glitch', TemplateView.as_view(template_name='clock_glitch.html'), name='glitch'),
    url(r'^flat', TemplateView.as_view(template_name='clock_flat.html'), name='flat'),
    url(r'^scss', TemplateView.as_view(template_name='clock_scss.html'), name='scss'),
    url(r'^mother', TemplateView.as_view(template_name='clock_mother.html'), name='mothers'),
    url(r'^round', TemplateView.as_view(template_name='clock_round.html'), name='round'),
    url(r'^date', TemplateView.as_view(template_name='clock_date.html'), name='date'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

