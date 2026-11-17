from html import unescape

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    # Har naye user ka profile khud ban jaye
    if created:
        Profile.objects.get_or_create(user=instance)


class PostQuerySet(models.QuerySet):
    def live(self):
        """Published posts + woh scheduled posts jinka waqt aa chuka hai."""
        now = timezone.now()
        return self.filter(
            Q(status="published") | Q(status="scheduled", publish_at__lte=now)
        )


class Post(models.Model):
    STATUS = [("draft", "Draft"), ("published", "Published"), ("scheduled", "Scheduled")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    body = RichTextField()
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    publish_at = models.DateTimeField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])

    @property
    def display_date(self):
        return self.publish_at or self.created

    @property
    def excerpt(self):
        text = unescape(strip_tags(self.body))
        return Truncator(text).words(35)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{self.name} on {self.post}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class DailyVisits(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "daily visits"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}: {self.count}"