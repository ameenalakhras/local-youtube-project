from django.db import models
from django.conf import settings

# Create your models here.

class Audio(models.Model):
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    url = models.URLField(max_length=512)
    originalurl = models.URLField(max_length=512,unique=True)
    youtube_id = models.CharField(max_length=100, unique=True)
    title = models.TextField()
    extend =models.CharField(max_length=50)
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
    # # featured_image = models.URLField(max_length=500)
    # name = models.CharField(max_length=255, null=True, blank=True)
    # size = models.IntegerField(null=True)
    # last_download_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
