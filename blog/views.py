from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from .forms import CommentForm, PostForm, SubscribeForm
from .models import Category, Post

User = get_user_model()


class PostListView(ListView):
    template_name = "blog/post_list.html"
    paginate_by = 5
    context_object_name = "posts"

    def get_queryset(self):
        qs = Post.objects.live().select_related("author", "category").prefetch_related("tags")
        if slug := self.kwargs.get("category_slug"):
            qs = qs.filter(category__slug=slug)
        if tag := self.kwargs.get("tag_slug"):
            qs = qs.filter(tags__slug=tag)
        if username := self.kwargs.get("username"):
            qs = qs.filter(author__username=username)
        return qs.order_by("-publish_at", "-created")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = "Latest Posts"
        if slug := self.kwargs.get("category_slug"):
            ctx["heading"] = f"Category: {get_object_or_404(Category, slug=slug).name}"
        if tag := self.kwargs.get("tag_slug"):
            ctx["heading"] = f"Tag: {tag}"
        if username := self.kwargs.get("username"):
            author = get_object_or_404(User, username=username)
            ctx["heading"] = f"Posts by {author.username}"
            ctx["author_profile"] = getattr(author, "profile", None)
        return ctx


class PostDetailView(FormMixin, DetailView):
    template_name = "blog/post_detail.html"
    form_class = CommentForm

    def get_queryset(self):
        qs = Post.objects.live()
        # Author apni draft posts preview kar sakta hai
        if self.request.user.is_authenticated:
            qs = qs | Post.objects.filter(author=self.request.user)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.filter(approved=True)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            messages.success(request, "Shukriya! Comment moderation ke baad nazar aayega.")
            return redirect(self.object.get_absolute_url())
        return self.form_invalid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class SubscribeView(FormView):
    form_class = SubscribeForm
    template_name = "blog/subscribe.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Subscribe ho gaye! Nayi post par email milegi.")
        return super().form_valid(form)
