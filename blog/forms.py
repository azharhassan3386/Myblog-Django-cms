from django import forms

from .models import Comment, Post, Subscriber


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "category", "body", "tags", "status", "publish_at"]
        widgets = {
            "publish_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["publish_at"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"]

    def clean(self):
        data = super().clean()
        if data.get("status") == "scheduled" and not data.get("publish_at"):
            self.add_error("publish_at", "Schedule ke liye date/time zaroori hai.")
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 4})}


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
