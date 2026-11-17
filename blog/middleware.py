from django.db.models import F
from django.utils import timezone

from .models import DailyVisits

SKIP_PREFIXES = ("/admin", "/static", "/media", "/feed", "/sitemap")


class VisitorCountMiddleware:
    """Har session ko din mein sirf ek baar count karta hai."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        today = str(timezone.localdate())
        if (
            request.method == "GET"
            and not request.path.startswith(SKIP_PREFIXES)
            and request.session.get("counted_today") != today
        ):
            obj, _ = DailyVisits.objects.get_or_create(date=timezone.localdate())
            DailyVisits.objects.filter(pk=obj.pk).update(count=F("count") + 1)
            request.session["counted_today"] = today
        return response
