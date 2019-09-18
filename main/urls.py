from django.conf.urls import  url
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.mainPage, name="mainPage"),
    path("downloadVideo", views.downloadVideo, name="downloadVideo"),
    path("browseVideos/", views.browseVideos, name="browseVideos"),
    path("experimentationPage/", views.experimentFunction, name="experimentPage"),
    path("hi/", views.upload_an_image_to_aws_experimentation),
    path("downloadVideoList", views.downloadVideoList, name="downloadVideoList"),
    path("record/<audio_id>/",views.audio_page, name="audio_page"),
    path("update_record/", views.update_audio_info, name="refresh_audio_info"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
