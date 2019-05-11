from django.conf import settings
from .models import Audio
import os

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


def createRecord(extracted_video_data, video_url):
    """
    create new record of Audio class in Data Base given the data
    """

    url = extracted_video_data.get("url", None)
    youtube_id = extracted_video_data.get("id", None)
    title = extracted_video_data.get('title', None)
    extend = extracted_video_data.get('ext', None)
    extractor = extracted_video_data.get("extractor", None)
    extractor_key = extracted_video_data.get("extractor_key", None)
    duration = extracted_video_data.get("duration", None)
    view_count = extracted_video_data.get("view_count", None)
    like_count = extracted_video_data.get("like_count", None)
    dislike_count = extracted_video_data.get("dislike_count", None)
    age_limit = extracted_video_data.get("age_limit", None)

    folderPath = "{}/{}/".format(settings.MEDIA_ROOT, extractor_key)
    mediaList = os.listdir(folderPath)
    check_results = [youtube_id in value for value in mediaList]
    fileNameIndex = check_results.index(True)
    fileName = mediaList[fileNameIndex]

    filePath = '{}/{}'.format(extractor_key,fileName)

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
    )

    return new_record, filePath

def checkRecordExists(videoURL):
    """
    check if the record exists or not in the dataBase
    """
    result = Audio.objects.filter(originalurl=videoURL).exists()
    return result


def getYoutubeDlOptions():
    return {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
                "outtmpl":"{}/%(extractor_key)s/%(id)s.%(ext)s".format(settings.MEDIA_ROOT), # the name of the saved file
            }

def catchSavingExcetions(new_record):
    """
    this function attemps to save the records with catching exceptions if they happen
    - new_record is the record to be saved
    """

    try:
        new_record.save()
    except IntegrityError as e:
        message = "record is saved already with this id"
        errorMessage = "exception happened which is :\n" + e

    except (DownloadError, HTTPError) as e:
        message = "couldn't get the file !"
        errorMessage = "exception happened which is :\n" + e

    except Exception as e:
        message = "a problem has occurred, please try again later"
        errorMessage = "a new exception happened which is :\n" + e
    else:
        message = "finished converting, the file is ready to use "
        errorMessage = None

    return message, errorMessage
