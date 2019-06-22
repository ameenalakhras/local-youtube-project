from __future__ import unicode_literals
import youtube_dl
import os
from django.conf import settings
from django.shortcuts import render
from .models import Audio
from django.db.utils import IntegrityError
from youtube_dl.utils import DownloadError
from requests.exceptions import HTTPError
from .youtubeDlFucntions import my_hook,MyLogger,createRecord, checkRecordExists, getYoutubeDlOptions, catchSavingExcetions
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_GET
from django.http import HttpResponseRedirect,JsonResponse

from .forms import UploadUrl as UploadVideoForm


def mainPage(request):
    """
    the main page of the website
    """
    audioRecords = Audio.objects.all()
    uploadForm = UploadVideoForm()
    context = {
        "audioRecords":audioRecords,
        "MEDIA_URL": settings.MEDIA_URL,
        "UploadUrl": uploadForm,

    }
    return render(request, template_name="mainPage.html" ,context=context )


@require_http_methods(["POST"])
def downloadVideo(request):
    """
    the download video button at the main page
    """
    videoURL = request.POST.get('question','')

    if checkRecordExists(videoURL) is True:
        return JsonResponse({
            "answer" : "video exists already",
        })

    else:
        YoutubeDlOptions = getYoutubeDlOptions()

        with youtube_dl.YoutubeDL(YoutubeDlOptions) as ydl:
            extractedVideoData = ydl.extract_info(videoURL, download=True)

        new_record, filePath = createRecord(extractedVideoData, videoURL)
        new_record.file.name = filePath

        savingReportMessage, errorMessage = catchSavingExcetions(new_record)
        #ToDo: add errorMessage to the cmd or file logger
        return JsonResponse({"answer":savingReportMessage,})


def browseVideos(request):
    audioRecords = Audio.objects.all()
    context = {
        "audioRecords":audioRecords,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, template_name="browseVideos.html" ,context=context )
