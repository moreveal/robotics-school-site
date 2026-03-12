from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import translation

class LanguageRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # already has language
        for lang, _ in settings.LANGUAGES:
            if path.startswith(f"/{lang}/"):
                return self.get_response(request)

        # determine preferred language
        lang = translation.get_language_from_request(request)

        if lang not in dict(settings.LANGUAGES):
            lang = settings.LANGUAGE_CODE

        return HttpResponseRedirect(f"/{lang}{path}")
