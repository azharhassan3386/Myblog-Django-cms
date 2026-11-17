from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .feeds import AtomPostsFeed, LatestPostsFeed
from .sitemaps import PostSitemap

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("category/<slug:category_slug>/", views.PostListView.as_view(), name="category"),
    path("tag/<slug:tag_slug>/", views.PostListView.as_view(), name="tag"),
    path("author/<str:username>/", views.PostListView.as_view(), name="author"),
    path("subscribe/", views.SubscribeView.as_view(), name="subscribe"),
    path("feed/rss/", LatestPostsFeed(), name="rss"),
    path("feed/atom/", AtomPostsFeed(), name="atom"),
    path("sitemap.xml", sitemap, {"sitemaps": {"posts": PostSitemap}}, name="sitemap"),
]
