from django.conf.urls import  url
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.mainPage, name="mainPage"),
    path("temp/", views.temp, name="tempPage"),
    path("downloadVideo", views.downloadVideo, name="downloadVideo"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
