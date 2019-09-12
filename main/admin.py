from django.contrib import admin
from .models import Audio, VideoList
# Register your models here.


class AudioAdmin(admin.ModelAdmin):
    search_fields = ('title', )


admin.site.register(Audio, AudioAdmin)
admin.site.register(VideoList)
