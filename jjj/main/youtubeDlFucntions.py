from django.conf import settings
from .models import Audio
import os
from django.db.utils import IntegrityError
from youtube_dl.utils import DownloadError
from requests.exceptions import HTTPError
import glob


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def get_download_status(d):
    """
    returns the download status (download percentage, eta)
    """
    downloadBytesPercentage = d["downloaded_bytes"] / d["total_bytes"]
    downloadOutputPercentage = int(round(downloadBytesPercentage, 2) *100)
    estimatedRemainingTime = d["eta"]
    return("download percentge: {}%      estimated remaining time: {} seconds".format(downloadOutputPercentage,estimatedRemainingTime))

def my_hook(d):
    """
    the hook works stimulantsly while downloading the file
    """

    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

    if d["status"] is "downloading":
        download_status = get_download_status(d)
        print(download_status)

def return_fileName_and_extention(folderPath, file_raw_name):
    """
    takes the media folder path and the file_raw_name(without extention)
    returns the save file name and it's extension.
    """
    pattern_match_files = glob.glob(f"{folderPath}{file_raw_name}.*")

    file_empty = len(pattern_match_files) is 0
    file_exists = len(pattern_match_files) is 1
    file_duplicated = len(pattern_match_files) > 1

    if file_empty:
        raise ValueError("file Doesn't exist")
    elif file_duplicated:
        print(f"file with path {pattern_match_files[0]} is duplicated\
         (maybe it exists in different formats **mp4, mkv, etc.)")
        file_exists = True
    elif file_exists:
        file_full_path = pattern_match_files[0]
        file_name = file_full_path.split(folderPath)[1]
        file_extention = file_name.split('.')[-1]

    return file_name, file_extention


def createRecord(extracted_video_data, video_url):
    """
    create new record of Audio class(in models.py) in the DataBase given the data
    """
    url = video_url
    youtube_id = extracted_video_data.get("id", None)
    title = extracted_video_data.get('title', None)
    extractor = extracted_video_data.get("extractor", None)
    extractor_key = extracted_video_data.get("extractor_key", None)
    duration = extracted_video_data.get("duration", None)
    view_count = extracted_video_data.get("view_count", None)
    like_count = extracted_video_data.get("like_count", None)
    dislike_count = extracted_video_data.get("dislike_count", None)
    age_limit = extracted_video_data.get("age_limit", None)

    folderPath = "{}/{}/".format(settings.MEDIA_ROOT, extractor_key)
    fileName, extend = return_fileName_and_extention(folderPath=folderPath, file_raw_name=youtube_id)
    filePath = '{}/{}'.format(extractor_key,fileName)

    image_url =  extracted_video_data.get("thumbnail", None)

    new_record = Audio(
        url=url,
        originalurl=video_url,
        youtube_id=youtube_id,
        title=title,
        extend=extend,
        extractor=extractor,
        extractor_key=extractor_key,
        duration=duration,
        view_count=view_count,
        like_count=like_count,
        dislike_count=dislike_count,
        age_limit=age_limit,
        image_url=image_url
    )
    if image_url is not None:
        new_record.get_remote_image()

    return new_record, filePath

def checkRecordExists(videoURL):
    """
    check if the record exists or not in the dataBase
    """
    result = Audio.objects.filter(originalurl=videoURL).exists()
    return result

def getYoutubeDlOptions(heightest_width=256):
    #  widths given the resolution
    # 	256.0 	144p
    #  	426.0 	240p
    #  	640.0 	360p
    #  	854.0 	480p
    # 	1280.0 	720p
    # 	640.0 	medium
    return {
                'format':f'-f bestvideo[width<={heightest_width}]/bestvideo+bestaudio/best',
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
                "outtmpl":f"{settings.MEDIA_ROOT}/%(extractor_key)s/%(id)s.%(ext)s", # the name of the saved file
            }

def catchSavingExcetions(new_record):
    """
    this function attemps to save the records with catching exceptions if they happen
    - new_record is the record to be saved
    """
    try:
        new_record.save()
        message = "finished converting, the file is ready to use "
        errorMessage = None

    except IntegrityError as e:
        message = "record is saved already with this id"
        errorMessage = "exception happened which is :\n" + str(e)

    except (DownloadError, HTTPError) as e:
        message = "couldn't get the file !"
        errorMessage = "exception happened which is :\n" + str(e)

    return message, errorMessage
