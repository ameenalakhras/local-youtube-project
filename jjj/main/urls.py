from django.conf.urls import  url
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.mainPage, name="mainPage"),
    path("downloadVideo", views.downloadVideo, name="downloadVideo"),
    path("browseVideos/", views.browseVideos, name="browseVideos")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
