from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand

from blog.models import Post, Subscriber


class Command(BaseCommand):
    help = "Nayi live posts ki email subscribers ko bhejta hai"

    def handle(self, *args, **opts):
        emails = list(Subscriber.objects.values_list("email", flat=True))
        domain = Site.objects.get_current().domain
        for post in Post.objects.live().filter(notified=False):
            msgs = [
                (
                    f"New post: {post.title}",
                    f"Padhein: http://{domain}{post.get_absolute_url()}",
                    settings.DEFAULT_FROM_EMAIL,
                    [e],
                )
                for e in emails
            ]
            if msgs:
                send_mass_mail(msgs)
            post.notified = True
            post.save(update_fields=["notified"])
            self.stdout.write(self.style.SUCCESS(f"Notified: {post.title} ({len(emails)} subscribers)"))
