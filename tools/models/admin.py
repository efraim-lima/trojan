from django.contrib import admin

# Register your models here.
from .models import Day, AppsLog, FileLog, KeywordsData, ImageData, VideoData, AudioData, ScreenImageData, ScreenVideoData, ScreenAudioData

admin.site.register(Day)
admin.site.register(AppsLog)
admin.site.register(FileLog)
admin.site.register(KeywordsData)
admin.site.register(ImageData)
admin.site.register(VideoData)
admin.site.register(AudioData)
admin.site.register(ScreenAudioData)
admin.site.register(ScreenImageData)
admin.site.register(ScreenVideoData)