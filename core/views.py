from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language

from .models import Course, CourseTranslation, Post, PostTranslation


def _current_language(request) -> str:
    return getattr(request, "LANGUAGE_CODE", None) or get_language() or settings.LANGUAGE_CODE


def _get_post_translation(post: Post, language: str) -> PostTranslation | None:
    """
    Return translation for requested language, or fallback to default
    language, or any available translation.
    """
    qs = post.translations.filter(language=language)
    if qs.exists():
        return qs.first()

    default_lang = settings.LANGUAGE_CODE
    if language != default_lang:
        qs = post.translations.filter(language=default_lang)
        if qs.exists():
            return qs.first()

    return post.translations.first()


def _get_course_translation(course: Course, language: str) -> CourseTranslation | None:
    qs = course.translations.filter(language=language)
    if qs.exists():
        return qs.first()

    default_lang = settings.LANGUAGE_CODE
    if language != default_lang:
        qs = course.translations.filter(language=default_lang)
        if qs.exists():
            return qs.first()

    return course.translations.first()


def home(request):
    language = _current_language(request)

    featured_post = (
        Post.objects.filter(
            is_published=True,
            is_featured=True,
        )
        .order_by("-published_at")
        .first()
    )

    latest_posts_qs = Post.objects.filter(is_published=True).order_by("-published_at")

    if featured_post:
        latest_posts_qs = latest_posts_qs.exclude(pk=featured_post.pk)

    latest_posts = list(latest_posts_qs[:3])

    featured_translation = (
        _get_post_translation(featured_post, language) if featured_post else None
    )

    latest_translated = []
    for post in latest_posts:
        tr = _get_post_translation(post, language)
        if tr:
            latest_translated.append(
                {
                    "slug": post.slug,
                    "published_at": post.published_at,
                    "title": tr.title,
                    "excerpt": tr.excerpt,
                }
            )

    return render(
        request,
        "home.html",
        {
            "featured_post": featured_post,
            "featured_translation": featured_translation,
            "latest_posts": latest_translated,
        },
    )


def news_list(request):
    language = _current_language(request)
    posts_qs = Post.objects.filter(is_published=True).order_by("-published_at")

    posts = []
    for post in posts_qs:
        tr = _get_post_translation(post, language)
        if not tr:
            continue
        posts.append(
            {
                "slug": post.slug,
                "published_at": post.published_at,
                "title": tr.title,
                "excerpt": tr.excerpt,
            }
        )

    return render(request, "news_list.html", {"posts": posts})


def news_detail(request, slug: str):
    language = _current_language(request)
    post = get_object_or_404(Post, slug=slug, is_published=True)
    translation = _get_post_translation(post, language)

    if not translation:
        # No translations at all – show 404 rather than an empty page
        raise get_object_or_404(PostTranslation, pk=-1)  # always 404

    return render(
        request,
        "news_detail.html",
        {
            "post": post,
            "translation": translation,
        },
    )


def courses_list(request):
    language = _current_language(request)
    courses_qs = Course.objects.filter(is_active=True).order_by("order", "slug")

    courses = []
    for course in courses_qs:
        tr = _get_course_translation(course, language)
        if not tr:
            continue
        courses.append(
            {
                "slug": course.slug,
                "title": tr.title,
                "short_description": tr.short_description,
                "age_range": tr.age_range,
                "schedule": tr.schedule,
                "image": course.image,
            }
        )

    return render(request, "courses_list.html", {"courses": courses})


def course_detail(request, slug: str):
    language = _current_language(request)
    course = get_object_or_404(Course, slug=slug, is_active=True)
    translation = _get_course_translation(course, language)

    if not translation:
        raise get_object_or_404(CourseTranslation, pk=-1)

    return render(
        request,
        "course_detail.html",
        {
            "course": course,
            "translation": translation,
        },
    )
