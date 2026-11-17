from html import unescape

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from django.utils.html import strip_tags

from .models import Post


class LatestPostsFeed(Feed):
    title = "My Blog"
    description = "Latest posts"

    def link(self):
        return reverse("post_list")

    def items(self):
        return Post.objects.live().order_by("-created")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return unescape(strip_tags(item.body))[:300]

    def item_pubdate(self, item):
        return item.display_date


class AtomPostsFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description