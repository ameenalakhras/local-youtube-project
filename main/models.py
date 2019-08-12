from django.db import models
from django.conf import settings
from tempfile import NamedTemporaryFile
from django.core.files import File
from urllib.request import urlopen
# Create your models here.

class Audio(models.Model):
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    url = models.URLField(max_length=512)
    originalurl = models.URLField(max_length=512,unique=True)
    youtube_id = models.CharField(max_length=100, unique=True)
    title = models.TextField()
    extend =models.CharField(max_length=50, null=True)
    extractor = models.CharField(max_length=30)
    extractor_key = models.CharField(max_length=30)
    duration = models.IntegerField(null=True)
    view_count = models.IntegerField(null=True)
    like_count = models.IntegerField(null=True)
    dislike_count = models.IntegerField(null=True)
    age_limit = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    last_download_date = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='{}'.format(settings.MEDIA_ROOT[1:]),null=True)
    image_file = models.ImageField(upload_to='{}'.format("images/"),null=True, blank=True)
    image_url = models.URLField(null=True)

    def __str__(self):
        return self.title

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            image_extention = self.image_url.split(".")[-1]
            self.image_file.save(f"{self.extractor_key}/{self.youtube_id}.{image_extention}", File(img_temp))


class VideoList(models.Model):
    list_type = models.CharField(max_length=300, null=True)
    list_id = models.CharField(max_length=300, unique=True)
    title = models.CharField(max_length=300)
    uploader = models.CharField(max_length=300)
    uploader_id = models.CharField(max_length=300)
    uploader_url = models.CharField(max_length=300)
    extractor = models.CharField(max_length=300)
    webpage_url = models.CharField(max_length=300)
    webpage_url_basename = models.CharField(max_length=300)
    extractor_key = models.CharField(max_length=300)
    create_date = models.DateTimeField(auto_now=True)
    videos = models.ManyToManyField(Audio, related_name="video_videoList_manyToMany", blank=True)

    class Meta:
        ordering = ('create_date',)

    def __str__(self):
        return self.title
