from urllib.parse import parse_qs, urlparse

from django import template


register = template.Library()


@register.filter
def embed_url(url: str) -> str:
    """
    Convert a regular YouTube URL (watch or youtu.be) to an embeddable URL.
    Falls back to the original URL if it cannot be parsed.
    """
    if not url:
        return ""

    try:
        parsed = urlparse(url)
    except Exception:
        return url

    host = (parsed.netloc or "").lower()

    # Standard YouTube watch URLs, e.g. https://www.youtube.com/watch?v=VIDEO_ID
    if "youtube.com" in host:
        # If it's already an /embed/ URL, just return as-is
        if parsed.path.startswith("/embed/"):
            return url

        query = parse_qs(parsed.query or "")
        video_id = (query.get("v") or [None])[0]

        # Shorts or other path-based formats, best-effort
        if not video_id and parsed.path.startswith("/shorts/"):
            parts = parsed.path.split("/")
            if len(parts) >= 3 and parts[2]:
                video_id = parts[2]

        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"

    # Short YouTube URLs, e.g. https://youtu.be/VIDEO_ID
    if "youtu.be" in host:
        video_id = parsed.path.lstrip("/")
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"

    # For now, return the URL unchanged for other providers (Vimeo, etc.)
    return url

