from django.contrib import admin
from .models import Video, VideoPublishedProxy, VideoAllProxy

# Register your models here.

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'state', 'video_id', 'is_published', 'get_playlist_ids']
    list_filter = ['active', 'state']
    search_fields = ['title']
    readonly_fields = ['id', 'is_published', 'publish_timestamp', 'get_playlist_ids']
    class Meta:
        model = VideoAllProxy

    #def published(self, obj, *args, **kwargs):
    #    return obj.active


admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']
    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)



admin.site.register(VideoPublishedProxy, VideoProxyAdmin)