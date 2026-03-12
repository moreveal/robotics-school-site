from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


def get_language_choices():
    return getattr(settings, "LANGUAGES", (("et", "Estonian"),))


class Post(models.Model):
    slug = models.SlugField(
        _("slug"),
        max_length=255,
        unique=True,
        help_text=_("Used in the news URL. Generated from title."),
    )
    is_published = models.BooleanField(_("published"), default=True)
    is_featured = models.BooleanField(
        _("show on home page"),
        default=False,
        help_text=_(
            "If enabled, this post will be highlighted on the home page for its language."
        ),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    published_at = models.DateTimeField(
        _("published at"),
        default=timezone.now,
        db_index=True,
    )

    class Meta:
        ordering = ("-published_at", "-created_at")
        verbose_name = _("news post")
        verbose_name_plural = _("news posts")

    def __str__(self) -> str:
        return self.slug


class PostTranslation(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name=_("post"),
    )
    language = models.CharField(
        _("language"),
        max_length=7,
        choices=get_language_choices(),
    )
    title = models.CharField(_("title"), max_length=255)
    excerpt = models.TextField(
        _("short summary"),
        blank=True,
        help_text=_("Optional short text shown in the news list."),
    )
    content = RichTextField(
        _("content (HTML allowed)"),
        help_text=_("Main text of the news post. You can paste formatted text."),
    )

    class Meta:
        unique_together = ("post", "language")
        verbose_name = _("news post translation")
        verbose_name_plural = _("news post translations")

    def __str__(self) -> str:
        return f"{self.post.slug} [{self.language}]"


class Course(models.Model):
    slug = models.SlugField(
        _("slug"),
        max_length=255,
        unique=True,
        help_text=_("Used in the course URL. Generated from title."),
    )
    image = models.ImageField(
        _("image"),
        upload_to="courses/",
        blank=True,
        null=True,
        help_text=_("Optional main image for the course."),
    )
    video_url = models.URLField(
        _("video URL"),
        blank=True,
        help_text=_("Optional link to a course video (YouTube, Vimeo, etc.)."),
    )
    is_active = models.BooleanField(_("active"), default=True)
    order = models.PositiveIntegerField(
        _("order"),
        default=0,
        help_text=_("Lower values appear first in the list."),
    )

    class Meta:
        ordering = ("order", "slug")
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self) -> str:
        return self.slug


class CourseTranslation(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name=_("course"),
    )
    language = models.CharField(
        _("language"),
        max_length=7,
        choices=get_language_choices(),
    )
    title = models.CharField(_("title"), max_length=255)
    short_description = models.TextField(
        _("short summary"),
        blank=True,
        help_text=_("Short intro text shown in the courses list."),
    )
    age_range = models.CharField(
        _("age range"),
        max_length=255,
        blank=True,
        help_text=_("Example: 6–8 aastat"),
    )
    schedule = models.CharField(
        _("schedule"),
        max_length=255,
        blank=True,
        help_text=_("Example: kord nädalas 90 min"),
    )
    locations = models.TextField(
        _("locations"),
        blank=True,
        help_text=_("Where the course takes place."),
    )
    content = RichTextField(
        _("content (HTML allowed)"),
        help_text=_("Full description of the course. You can paste formatted text."),
    )

    class Meta:
        unique_together = ("course", "language")
        verbose_name = _("course translation")
        verbose_name_plural = _("course translations")

    def __str__(self) -> str:
        return f"{self.course.slug} [{self.language}]"
