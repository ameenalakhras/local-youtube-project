from django.conf import settings
from .models import Audio, VideoList
import os
from django.db.utils import IntegrityError
from youtube_dl.utils import DownloadError
from requests.exceptions import HTTPError
import glob
# import moviepy.editor as mpe
from moviepy.editor import *



def combineVideoAndAudio(folderPath, video_file,audio_file, file_raw_name):

    videoclip = VideoFileClip(folderPath+video_file)
    audioclip = AudioFileClip(folderPath+audio_file)

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip

    new_file_extention = "mp4"
    new_file_path = f"{folderPath}{file_raw_name}.{new_file_extention}"
    videoclip.write_videofile(new_file_path)

    return new_file_path, new_file_extention


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
    # if youtube_dl created two files instead of one (video file and audio file) ('webm' file and 'mp4' file)
    elif file_duplicated:
        print(f"file with path {pattern_match_files[0]} is duplicated\
         (maybe it exists in different formats **mp4, mkv, etc.)")
        file_exists = True
        first_file = pattern_match_files[0]
        second_file = pattern_match_files[1]

        if firstfile.endswith(".mp4"):
            video_file = firstfile
            audio_file = second_file
        else:
            video_file = second_file
            audio_file = first_file

        file_name, file_extention = combineVideoAndAudio(folderPath, video_file,audio_file, file_raw_name)


    elif file_exists:
        file_full_path = pattern_match_files[0]
        file_name = file_full_path.split(folderPath)[1]
        file_extention = file_name.split('.')[-1]

    return file_name, file_extention


def createRecord(extracted_video_data, video_url, save=True):
    """
    create new record of Audio class(in models.py) in the DataBase given the data
    """
    youtube_id = extracted_video_data.get("id", None)

    record_exists = Audio.objects.filter(youtube_id=youtube_id).exists()
    if record_exists:
        new_record = Audio.objects.get(youtube_id=youtube_id)
        try:
            filePath = new_record.file.name
        except:
            filePath = None
        return new_record, filePath


    url = video_url
    title = extracted_video_data.get('title', None)
    extractor = extracted_video_data.get("extractor", None)
    extractor_key = extracted_video_data.get("extractor_key", None)
    duration = extracted_video_data.get("duration", None)
    view_count = extracted_video_data.get("view_count", None)
    like_count = extracted_video_data.get("like_count", None)
    dislike_count = extracted_video_data.get("dislike_count", None)
    age_limit = extracted_video_data.get("age_limit", None)

    folderPath = "{}/{}/".format(settings.MEDIA_ROOT, extractor_key)
    if save:
        fileName, extend = return_fileName_and_extention(folderPath=folderPath, file_raw_name=youtube_id)
        filePath = '{}/{}'.format(extractor_key,fileName)
    else:
        filePath=None
        extend=None

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


def createVideoList(extracted_video_data):
    list_type = extracted_video_data.get("list_type", None)
    list_id = extracted_video_data.get("id", None)
    title = extracted_video_data.get("title", None)
    uploader = extracted_video_data.get("uploader", None)
    uploader_id = extracted_video_data.get("uploader_id", None)
    uploader_url = extracted_video_data.get("uploader_url", None)
    extractor = extracted_video_data.get("extractor", None)
    webpage_url = extracted_video_data.get("webpage_url", None)
    webpage_url_basename = extracted_video_data.get("webpage_url_basename", None)
    extractor_key = extracted_video_data.get("extractor_key", None)

    new_video_list_record = VideoList(
        list_type=list_type,
        list_id=list_id,
        title=title,
        uploader=uploader,
        uploader_id=uploader_id,
        uploader_url=uploader_url,
        extractor=extractor,
        webpage_url=webpage_url,
        webpage_url_basename=webpage_url_basename,
        extractor_key=extractor_key,
    )

    new_video_list_record.save()

    return new_video_list_record


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

# PLLMjTMpBr4H1I2hUXnKvtp5m9JO07pz9V
# def getYoutubeDlOptions(heightest_width=256):
#     #  widths given the resolution
#     # 	256.0 	144p
#     #  	426.0 	240p
#     #  	640.0 	360p
#     #  	854.0 	480p
#     # 	1280.0 	720p
#     # 	640.0 	medium
#     return {
#                 'format':f'-f bestvideo[width<={heightest_width}]/bestvideo+bestaudio/best',
#                 'logger': MyLogger(),
#                 'progress_hooks': [my_hook],
#                 "outtmpl":f"{settings.MEDIA_ROOT}/%(extractor_key)s/%(id)s.%(ext)s", # the name of the saved file
#             }
#

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


def checkUrlType(text):
    """ check if the inputted is a URL or a video ID """

    if ("&list=" in text) and ("playlist" not in text):
        text_type = "video_in_playlist"

    elif ("youtube" in text) and ("watch?v" in text)  :
        text_type = "video"

    elif "playlist" in text:
        text_type = "playlist" # &list=WL

    elif "." not in text:
        text_type = "video_id"

    else:
        raise ValueError("URL isn't valid, please make sure it's a youtube video url.")

    return text_type


def get_video_url_from_link(text, video_id=None):
    """
        checks the type of the link using checkUrlType then transforms it into a downloadable video url
    """

    video_type = checkUrlType(text)
    if video_type is "video":
        video_url = text
    elif video_type is "video_in_playlist":
        video_url = text.split("&list")[0]
    elif video_type is "playlist":
        pass
    elif video_type is "video_id":
        # the text is the video_id here
        video_url = f"https://www.youtube.com/watch?v={text}"
    else:
        raise ValueError("video type isn't recognized")

    return video_url


def playlistOptions():
    # playlistreverse
    return {
                # 'format':'--flat-playlist -j --skip-download',
                'logger': MyLogger(),
                # 'progress_hooks': [my_hook],
                "outtmpl":f"{settings.BASE_DIR}/result.log", # the name of the saved file
            }
