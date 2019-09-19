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
    ###extra keys for more usage ..:
    ## ["_speed_str"] # kiB/second  ## ["_total_bytes_str"] ##["_eta_str"]
    downloadOutputPercentage = d["_percent_str"]
    estimatedRemainingTime = d["_eta_str"]
    return("download percentge: {}     estimated remaining time: {}".format(downloadOutputPercentage,estimatedRemainingTime))


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


def createRecord(extracted_video_data, save=True, update_data=False):
    """
    create new record of Audio class(in models.py) in the DataBase given the data
    if the record exists > it returns the existed record
    return the mp4 file path and the new record.
    it also updates the record columns if update_data is true.
    """
    extractor_key = extracted_video_data.get("extractor_key", None)
    youtube_id = extracted_video_data.get("id", None)
    record_exists = Audio.objects.filter(youtube_id=youtube_id).exists()

    if record_exists and (update_data is False):
        new_record = Audio.objects.get(youtube_id=youtube_id)
        try:
            filePath = new_record.file.name
            file_exists = True
        except:
            file_exists = False

        if (file_exists is False) or (filePath is ''):
            check = check_file_exists_and_not_connected_to_database(record = new_record)
            if check["status"] is False:
                filePath = None
            else:
                filePath = check["filePath"]
        return new_record, filePath



    url = generate_youtube_url(youtube_id)
    title = extracted_video_data.get('title', None)
    extractor = extracted_video_data.get("extractor", None)
    duration = extracted_video_data.get("duration", None)
    view_count = extracted_video_data.get("view_count", None)
    like_count = extracted_video_data.get("like_count", None)
    dislike_count = extracted_video_data.get("dislike_count", None)
    age_limit = extracted_video_data.get("age_limit", None)
    image_url =  extracted_video_data.get("thumbnail", None)

    if update_data:
        new_record = Audio.objects.get(youtube_id=youtube_id)
        new_record.url = url
        new_record.originalurl = url
        new_record.youtube_id = youtube_id
        new_record.title = title
        new_record.extractor = extractor
        new_record.extractor_key = extractor_key
        new_record.duration = duration
        new_record.view_count = view_count
        new_record.like_count = like_count
        new_record.dislike_count = dislike_count
        new_record.age_limit = age_limit
        new_record.image_url = image_url

        image_doesnt_exist = (image_url is not None) and ( (new_record.image_file == None) or (new_record.image_file.name == '') )

        if image_doesnt_exist:
            new_record.get_remote_image()

        filePath = None

    else:

        folderPath = "{}/{}/".format(settings.MEDIA_ROOT, extractor_key)
        if save:
            fileName, extend = return_fileName_and_extention(folderPath=folderPath, file_raw_name=youtube_id)
            filePath = '{}/{}'.format(extractor_key,fileName)
        else:
            filePath=None
            extend=None

        new_record = Audio(
            url=url,
            originalurl=url,
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

        new_record.extend = extend

        if image_url is not None:
            new_record.get_remote_image()

    return new_record, filePath


def createVideoList(extracted_video_data):
    """ create a video List with its info (videos aren't included
        using this function) """
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

def extract_youtube_id_from_url(url):
    """extracts the video id from a video url"""
    video_id = url.split("watch?v=")[1]
    video_id = video_id.split("/")[0] # trim anything after the video id
    return video_id

def checkRecordExists(video_id, entry_type="youtube_id"):
    """
    check if the record exists or not in the dataBase
    """
    if entry_type == "youtube_id":
        record_exists = Audio.objects.filter(youtube_id=video_id).exists()
    elif entry_type == "database_id":
        if type(video_id) == str:
            video_id = int(video_id)
        record_exists = Audio.objects.filter(id=video_id).exists()
    else:
        raise ValueError("entry type doesn't exist")

    return record_exists

def checkRecordFileExists(video_id, entry_type="youtube_id"):
    """Checks if the record video file exists """

    if entry_type == "youtube_id":
        record = Audio.objects.filter(youtube_id=video_id).first()
    elif entry_type == "database_id":
        if type(video_id) == str:
            video_id = int(video_id)
        record = Audio.objects.filter(id=video_id).first()

    try:
        file = record.file.name
        file_exists = True
        if file == '':
            file_exists = False
    except:
        file_exists = False


    return file_exists



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
        message = f"record is saved already with this id, the litteral problem is {str(e)}"
        # errorMessage = "exception happened which is :\n" + str(e)
        errorMessage = "the file already exists, if the problem appears a lot report to the website developer please"

    except (DownloadError, HTTPError) as e:
        message = f"couldn't get the file (which is {str(e)})!"
        errorMessage = "a problem has happened while saving the file, please try again later"

    print(f"the hidden error message is:\n {message}")
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


def check_empty_file_field(file_field):
    """ Check if the file in django FileField is empty """

    empty_file = ""

    if file_field.file.name is empty_file:
        return True
    else:
        return False

def check_file_exists_and_not_connected_to_database(record):
    """ a bug might happen(it happened once) that the file physically exists
        but it's location is not added to the database file (this function will
        solve this problem if it happens) """

    folderPath = "{}/{}/".format(settings.MEDIA_ROOT, record.extractor_key)
    try:
        file_name, file_extention = return_fileName_and_extention(folderPath=folderPath, file_raw_name=record.youtube_id)
        file_exists = True
    # if file doesn't exist
    except ValueError:
        file_exists = False

    if file_exists:
        extractor_key = record.extractor_key
        filePath = '{}/{}'.format(extractor_key,file_name)
        return {'status': True, "filePath": filePath}
    else:
        return {"status": False}

def generate_youtube_url(video_id):
    """generate a youtube url given the video id"""
    video_url = f"""https://www.youtube.com/watch?v={video_id}"""
    return video_url
