from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Category
from playlists.models import Playlist, PlaylistItem
from playlists.mixins import PlaylistMixin

# Create your views here.
class CategoryListView(PlaylistMixin, ListView):
    queryset = Category.objects.all().filter(active=True).annotate(pl_count=Count('playlists')).filter(pl_count__gte=1)


class CategoryDetailView(PlaylistMixin, ListView):
    queryset = Category.objects.all().filter(active=True)

    def get_context_data(self):
        context = super().get_context_data()
        try:
            obj = Category.objects.get(slug=self.kwargs.get('slug'))
        except Category.DoesNotExist:
            raise Http404
        except Category.MultipleObjectsReturned:
            raise Http404
        except:
            obj = None
        context['object'] = obj
        if obj is not None:
            context['title'] = obj.title
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Playlist.objects.filter(category__slug=slug).movie_or_show()
