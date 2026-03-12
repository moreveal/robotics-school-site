from django.conf import settings
from django.contrib import admin

from .models import Course, CourseTranslation, Post, PostTranslation


class PostTranslationInline(admin.StackedInline):
    model = PostTranslation
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("slug", "is_published", "is_featured", "published_at")
    list_filter = ("is_published", "is_featured")
    date_hierarchy = "published_at"
    search_fields = ("slug", "translations__title", "translations__excerpt")
    ordering = ("-published_at",)
    inlines = [PostTranslationInline]


class CourseTranslationInline(admin.StackedInline):
    model = CourseTranslation
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("slug", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("slug", "translations__title", "translations__short_description")
    ordering = ("order", "slug")
    inlines = [CourseTranslationInline]
