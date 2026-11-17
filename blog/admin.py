from django.contrib import admin

from .models import Category, Comment, DailyVisits, Post, Profile, Subscriber


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "publish_at", "created")
    list_filter = ("status", "category")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "approved", "created")
    list_filter = ("approved",)
    actions = ["approve"]

    @admin.action(description="Selected comments approve karo")
    def approve(self, request, queryset):
        queryset.update(approved=True)


@admin.register(DailyVisits)
class DailyVisitsAdmin(admin.ModelAdmin):
    list_display = ("date", "count")


admin.site.register([Profile, Subscriber])
