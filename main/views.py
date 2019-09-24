from __future__ import unicode_literals
import youtube_dl
import os
from django.conf import settings
from django.shortcuts import render
from main.models import Audio, VideoList
from django.db.utils import IntegrityError
from youtube_dl.utils import DownloadError
from requests.exceptions import HTTPError
from main.youtubeDlFucntions import my_hook, MyLogger, createRecord, checkRecordExists,\
                                    getYoutubeDlOptions, catchSavingExcetions,\
                                    checkUrlType, playlistOptions, createVideoList,\
                                    get_video_url_from_link, generate_youtube_url,\
                                    extract_youtube_id_from_url, checkRecordFileExists
from django.views.decorators.http import require_http_methods, require_GET
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect
from main.forms import DownloadUrl as DownloadVideoForm
from main.forms import DownloadListUrl as DownloadVideoListForm

from main.utils import AWS


def mainPage(request):
    """
    the main page of the website
    """
    audioRecords = Audio.objects.all()
    videos_source = [(settings.MEDIA_URL + record.file.name) for record in  audioRecords]


    thumbnail_urls = [(settings.MEDIA_URL + (record.image_file.name or ""))  for record in  audioRecords]
    titles = [record.title for record in  audioRecords]

    DownloadForm = DownloadVideoForm()
    download_video_list_form = DownloadVideoListForm()

    context = {
        # "audioRecords":audioRecords,
        "thumbnail_urls":thumbnail_urls,
        "titles":titles,
        "videos_source": videos_source,
        "DownloadUrl": DownloadForm,
        "download_video_list_form": download_video_list_form,


    }
    return render(request, template_name="mainPage.html" ,context=context )


@require_http_methods(["POST"])
def downloadVideo(request):
    """
    the download video button at the main page
    """
    videoURL = request.POST.get('question','')
    video_id = extract_youtube_id_from_url(videoURL)

    file_exists = False
    record_exists = checkRecordExists(video_id, entry_type="youtube_id")
    if record_exists:
        file_exists = checkRecordFileExists(video_id, entry_type="youtube_id")
        print(file_exists)


    if (record_exists and file_exists) is True:
        return JsonResponse({
            "answer" : "video exists already",
        })

    else:
        YoutubeDlOptions = getYoutubeDlOptions()

        with youtube_dl.YoutubeDL(YoutubeDlOptions) as ydl:
            try:
                extractedVideoData = ydl.extract_info(videoURL, download=True)
            except DownloadError as e:
                response = JsonResponse({
                        "answer": {
                            "message": "couldn't download the video, please try again later"
                        },
                    })
                response.status_code = 403
                return response



        new_record, filePath = createRecord(extractedVideoData)
        new_record.file.name = filePath

        savingReportMessage, errorMessage = catchSavingExcetions(new_record)
        #ToDo: add errorMessage to the cmd or file logger
        return JsonResponse({"answer":savingReportMessage,})


def browseVideos(request):
    audioRecords = Audio.objects.all()

    videos_source = [(settings.MEDIA_URL + record.file.name) for record in  audioRecords]
    thumbnail_urls = [(settings.MEDIA_URL + (record.image_file.name or ""))  for record in  audioRecords]
    titles = [record.title for record in  audioRecords]

    context = {
        "audioRecords":audioRecords,
        "MEDIA_URL": settings.MEDIA_URL,
        "thumbnail_urls":thumbnail_urls,
        "titles":titles,
        "videos_source": videos_source,
    }
    return render(request, template_name="browseVideos.html" ,context=context )


def experimentFunction(request):
    """ this function is for site experimntation and for feature preperations """
    video_lists = VideoList.objects.all()
    # empty_audio_query = Audio.objects.filter(id=-1)
    # import ipdb; ipdb.set_trace()
    # audioRecords = empty_audio_query

    # all_videos_sources = []
    # all_thumbnail_urls = []
    # all_titles = []

    # for video_list in video_lists:
    #     # appends the "video_list" videos to "all_videos"
    #     audioRecords = video_list.videos.all()
    #
    #     for record in audioRecords:
    #         all_videos_sources.append(settings.MEDIA_URL + record.file.name)
    #         all_thumbnail_urls.append(settings.MEDIA_URL + (record.image_file.name or ""))
    #         all_titles.append(record.title)


    # playlistOptions()
    # import ipdb; ipdb.set_trace()
    context = {
        "video_lists": video_lists,
        # "MEDIA_URL": settings.MEDIA_URL,
        # "thumbnail_urls":all_thumbnail_urls,
        # "titles":all_titles,
        # "videos_source": all_videos_sources,

    }
    return render(request, template_name="videosLists.html" ,context=context )


@require_http_methods(["POST"])
def downloadVideoList(request):
    """
    the download video list button at the main page
    """

    listURL = request.POST.get('question','')
    # listURL = "https://www.youtube.com/playlist?list=PLLMjTMpBr4H1I2hUXnKvtp5m9JO07pz9V"


    YoutubeDlOptions = playlistOptions()

    with youtube_dl.YoutubeDL({"dump_single_json": True,
                            "j":True}) as ydl:
        try:
            extractedVideosListData = ydl.extract_info(listURL, download=False)
        except DownloadError as e :
            response = JsonResponse({"answer":"couldn't download the list, maybe it's not a public playlist !",})
            response.status_code = 403
            return response


    list_exists = VideoList.objects.filter(list_id=extractedVideosListData["id"]).exists()

    if list_exists:
        new_videolist_record = VideoList.objects.get(list_id=extractedVideosListData["id"])
    else:
        new_videolist_record = createVideoList(extractedVideosListData)


    error_messages = []
    savingReportMessages = []
    for extractedVideoData in extractedVideosListData["entries"]:
        origional_url = get_video_url_from_link(extractedVideoData["id"])

        new_record, _ = createRecord(extractedVideoData, save=False)

        # new_record.file.name = filePath
        #
        savingReportMessage, errorMessage = catchSavingExcetions(new_record)

        if errorMessage is None:
            # add the video to the videoList
            new_videolist_record.videos.add(new_record)
        else:
            savingReportMessages.append(savingReportMessage)
            error_messages.append(errorMessage)

    if len(savingReportMessages) == 0:
            savingReportMessages = "Everything is great, please enjoy the download"
    else:
        savingReportMessages = str(savingReportMessages)

    # #ToDo: add errorMessage to the cmd or file logger
    return JsonResponse({"answer":savingReportMessages,})
    # redirect("www.google.com")

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

@require_http_methods(["GET"])
def audio_page(request, audio_id):
    video = Audio.objects.get(id=audio_id)
    context = {
        "video": video,
        "MEDIA_URL": settings.MEDIA_URL
    }

    return render(request, template_name="Audio.html" ,context=context )

@require_http_methods(["POST"])
def update_audio_info(request):
    """ takes the audio id and updates all of its info but the video and image files"""
    audio_id = request.POST.get('question','')
    file_exists = False
    record_exists = checkRecordExists(audio_id, entry_type="database_id")
    if record_exists:
        file_exists = checkRecordFileExists(audio_id, entry_type="database_id")

    if record_exists  is False:
        return JsonResponse({
            "answer" : "video doesn't exists !",
        })
    else:
        youtube_url_id = Audio.objects.get(id=audio_id).youtube_id
        videoURL = generate_youtube_url(youtube_url_id)

        YoutubeDlOptions = getYoutubeDlOptions()

        with youtube_dl.YoutubeDL(YoutubeDlOptions) as ydl:
            extractedVideoData = ydl.extract_info(videoURL, download=False)
        # import ipdb; ipdb.set_trace()
        new_record, _ = createRecord(extractedVideoData, update_data=True)

        savingReportMessage, errorMessage = catchSavingExcetions(new_record)
        #ToDo: add errorMessage to the cmd or file logger
        return JsonResponse({"answer":savingReportMessage,})
