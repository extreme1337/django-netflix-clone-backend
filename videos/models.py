from datetime import time
from django.db import models
from django.db.models.fields import proxy
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class VideoQuerySet(models.QuerySet):
    def published(self):
        return self.filter(state=Video.VideoStateOptions.PUBLISH, publish_timestapm__lte=timezone.now()
        )


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

class PublishStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'


class Video(models.Model):
    VideoStateOptions = PublishStateOptions
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)


    objects = VideoManager()

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.active

    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
            print('save as published')
            self.publish_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None

        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'
