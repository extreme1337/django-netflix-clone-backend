from django.contrib import admin
from django.db import models
from tags.admin import TaggedItemInLine
from .models import MovieProxy, Playlist, PlaylistItem, TVShowSeasonProxy, TVShowProxy
# Register your models here.
class MovieProxyAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'description', 'state', 'category', 'video', 'slug']
    class Meta:
        model = MovieProxy

    def get_queryset(self, request):
        return MovieProxy.objects.all()

class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0
    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()

class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [SeasonEpisodeInline]
    list_display = ['title', 'parent']
    class Meta:
        models = TVShowSeasonProxy

admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)

class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields = ['order', 'title', 'state']

class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInLine, TVShowSeasonProxyInline]
    list_display = ['title']
    fields = ['title', 'description', 'state', 'category', 'video', 'slug']
    class Meta:
        model = TVShowProxy

    def get_queryset(self, request):
        return TVShowProxy.objects.all()

admin.site.register(TVShowProxy, TVShowProxyAdmin)

class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0

class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistItemInline]
    class Meta:
        model = Playlist

    def get_quertset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

admin.site.register(Playlist, PlaylistAdmin)
