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

# idjango.db.utils.IntegrityError

# Create your views here.

def mainPage(request):
    """
    the main page of the website
    """
    audioRecords = Audio.objects.all()
    context = {"audioRecords":audioRecords, "MEDIA_URL": settings.MEDIA_URL}
    return render(request, template_name="mainPage.html" ,context=context )


@require_http_methods(["POST"])
def downloadVideo(request):
    """
    the download video button at the main page
    """
    videoURL = request.POST.get('question','')

    if checkRecordExists(videoURL) is True:
        return JsonResponse({"answer" : "video exists already"})

    else:
        YoutubeDlOptions = getYoutubeDlOptions()

        with youtube_dl.YoutubeDL(YoutubeDlOptions) as ydl:
            extractedVideoData = ydl.extract_info(videoURL, download=True)

        new_record, filePath = createRecord(extractedVideoData, videoURL)
        new_record.file.name = filePath

        savingReportMessage, errorMessage = catchSavingExcetions(new_record)
        #ToDo: add errorMessage to the cmd or file logger

        return JsonResponse({"answer":savingReportMessage,})

def temp(request):
    """
    a temporary function for adding new features
    """

    ydl_opts = getYoutubeDlOpts()


    video_url = "https://www.youtube.com/watch?v=60ItHLz5WEA"

    if checkRecordExists(video_url) is True:
        print("this video is already added ")
        return render(request, template_name="temp.html", context=None)


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)

    new_record = createRecord(extracted_video_data)
    new_record.file.name = filePath
    try:
        new_record.save()
    except IntegrityError:
        print("record is saved already with this id")
    except (DownloadError, HTTPError):
        print("couldn't get the file !")
    except Exception as e:
        print(e)
    # ydl.download(['https://www.youtube.com/watch?v=-FyjEnoIgTM'])

    print("finished converting, the file is ready to use ")

    return render(request, template_name="temp.html", context=None)



# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404
#
# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404
#
#
# def getVideo(request):
#
#     response = download(request, path)
#     return None
