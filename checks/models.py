import uuid
import logging

from django.db import models

logger = logging.getLogger(__name__)


class Check(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    url = models.URLField()
    no_of_recommendations = models.IntegerField(default=0)

    # Checks
    debug_enabled = models.BooleanField()
    http_supported = models.BooleanField(null=True)
    https_supported = models.BooleanField()
    hsts_header_found = models.BooleanField()
    xframe_header_found = models.BooleanField()
    admin_found = models.BooleanField()
    admin_forces_https = models.BooleanField(null=True)
    login_found = models.BooleanField()
    login_forces_https = models.BooleanField(null=True)
    trace_allowed = models.BooleanField()
    csrf_cookie_found = models.BooleanField()
    session_cookie_found = models.BooleanField()
    session_cookie_secure = models.BooleanField(null=True)
    session_cookie_httponly = models.BooleanField(null=True)

    def update_recommendation_count(self):
        self.no_of_recommendations = 0
        logger.debug(f"{self.url=} : {self.no_of_recommendations=}")

        if self.debug_enabled:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.debug_enabled=} : {self.no_of_recommendations=}"
            )

        if not self.http_supported:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.http_supported=} : {self.no_of_recommendations=}"
            )

        if not self.https_supported:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.https_supported=} : {self.no_of_recommendations=}"
            )

        if not self.hsts_header_found:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.hsts_header_found=} : {self.no_of_recommendations=}"  # noqa
            )

        if not self.xframe_header_found:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.xframe_header_found=} : {self.no_of_recommendations=}"  # noqa
            )

        if self.admin_found and not self.admin_forces_https:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.admin_found=} : {self.admin_forces_https=} : {self.no_of_recommendations=}"  # noqa
            )

        if self.login_found and not self.login_forces_https:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.login_found=} : {self.login_forces_https=} : {self.no_of_recommendations=}"  # noqa
            )

        if self.trace_allowed:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.trace_allowed=} : {self.no_of_recommendations=}"
            )

        if not self.csrf_cookie_found:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.csrf_cookie_found=} : {self.no_of_recommendations=}"  # noqa
            )

        if self.session_cookie_found and not self.session_cookie_secure:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.session_cookie_found=} : {self.session_cookie_secure=} : {self.no_of_recommendations=}"  # noqa
            )

        if self.session_cookie_found and not self.session_cookie_httponly:
            self.no_of_recommendations += 1
            logger.debug(
                f"{self.url=} : {self.session_cookie_found=} : {self.session_cookie_httponly=} : {self.no_of_recommendations=}"  # noqa
            )

    @property
    def secure_percentage(self):
        # The calculation: Divide 100 by the number of possible recommendations and
        # then times by the number of recomendations. This number is rounded and then
        # subtracted from 100 to give the overall rating as a percentage. No
        # recommendations would be a 100 rating, all recommendations would be a 0
        # rating.
        return int(100 - round((100 / 11) * self.no_of_recommendations))

    @property
    def django_confirmed(self):
        # If any of these are true, we know it's Django
        return (
            self.debug_enabled
            or self.csrf_cookie_found
            or self.session_cookie_found
            or self.admin_found
        )
