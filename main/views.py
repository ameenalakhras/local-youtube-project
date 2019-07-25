from __future__ import unicode_literals
import youtube_dl
import os
from django.conf import settings
from django.shortcuts import render
from .models import Audio
from django.db.utils import IntegrityError
from youtube_dl.utils import DownloadError
from requests.exceptions import HTTPError
from .youtubeDlFucntions import my_hook,MyLogger,createRecord, checkRecordExists,\
                                getYoutubeDlOptions, catchSavingExcetions,\
                                checkUrlType
from django.views.decorators.http import require_http_methods, require_GET
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect
from .forms import UploadUrl as UploadVideoForm

from main.utils import AWS

def mainPage(request):
    """
    the main page of the website
    """
    audioRecords = Audio.objects.all()
    videos_source = [(settings.MEDIA_URL + record.file.name) for record in  audioRecords]
    # import ipdb; ipdb.set_trace()

    thumbnail_urls = [(settings.MEDIA_URL + (record.image_file.name or ""))  for record in  audioRecords]
    titles = [record.title for record in  audioRecords]

    uploadForm = UploadVideoForm()
    context = {
        # "audioRecords":audioRecords,
        "thumbnail_urls":thumbnail_urls,
        "titles":titles,
        "videos_source": videos_source,
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

def experimentFunction(request):
    """ this function is for site experimntation and for feature preperations """
    audioRecords = Audio.objects.all()
    videos_source = [(settings.MEDIA_URL + record.file.name) for record in  audioRecords]
    uploadForm = UploadVideoForm()
    context = {
        # "audioRecords":audioRecords,
        "videos_source": videos_source,
        "UploadUrl": uploadForm,

    }
    return render(request, template_name="experimentPage.html" ,context=context )


def upload_an_image_to_aws_experimentation(request):
    aws_id = settings.S3_KEY
    aws_password = settings.S3_SECRET_ACCESS_KEY
    aws_bucket = settings.S3_BUCKET

    aws_client = AWS(aws_id, aws_password)

    path_to_file = settings.MEDIA_URL
    file_name = "Youtube/y83x7MgzWOA.mp3"
    file_root = settings.STATIC_ROOT
    file_path = file_root + path_to_file + file_name

    with open(file_path, 'rb') as f:
        file = f.read()
        status = aws_client.upload_image_or_mp3_to_aws(filename=file_name, img_data = file, S3_BUCKET = settings.S3_BUCKET, content_type="mp3")

    print(f"the status is {status}")

    print("hi")

    return redirect("www.google.com")
