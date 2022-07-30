from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


# Create your models here.

class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    STATUS_PUBLISH = "published"
    STATUS_DRAFT = "draft"
    STATUS_CHOICES = (
        (STATUS_PUBLISH, "Published"),
        (STATUS_DRAFT, "Draft"),
    )
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post")
    body = RichTextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    object = models.Manager()
    published = PublishManager()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"{self.name} on {self.post}"
