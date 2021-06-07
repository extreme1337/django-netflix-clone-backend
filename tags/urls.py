from django.urls import path

from .views import TaggedItemListView

urlpatterns = [
    path("<slug:tag>", TaggedItemListView.as_view()),
    path('', TaggedItemListView.as_view()),
]
