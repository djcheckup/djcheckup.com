from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    # path("accounts/", include("allauth.urls")),
    path("django-rq/", include("django_rq.urls")),
    path("check/", include("checks.urls")),
    path("", include("website.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
