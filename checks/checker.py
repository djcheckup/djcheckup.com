import requests
import logging
import math
from urllib.parse import urljoin, urlparse

from django_rq import job
from rq import get_current_job


from .models import Check


logger = logging.getLogger(__name__)


class SecurityChecker(object):
    @job("checks")
    def run_check(self, url):

        # num_checks used to calculate progress and rating score
        num_checks = 11

        job = get_current_job()
        logger.debug(f"{job=}")

        self.update_progress(
            job, {"progress": 1, "current_status": "Starting checks..."}
        )

        self.session = requests.session()
        self.session.headers = [("User-agent", "DJ Checkup - https://djcheckup.com/")]

        try:
            homepage = self.session.get(url, timeout=7)
            logger.debug(f"{homepage=}")

            check_record = Check(url=url)

            # HSTS Header
            self.update_progress(
                job,
                {
                    "progress": math.ceil(2 / num_checks * 99),
                    "current_status": "Checking for HSTS header...",
                },
            )
            check_record.hsts_header_found = self.check_supports_hsts(url)
            logger.debug(f"{check_record.hsts_header_found=}")

            # Xframe Header
            self.update_progress(
                job,
                {
                    "progress": math.ceil(3 / num_checks * 99),
                    "current_status": "Checking for Xframe header...",
                },
            )
            check_record.xframe_header_found = (
                True if "X-Frame-Options" in homepage.headers else False
            )
            logger.debug(f"{check_record.xframe_header_found=}")

            # HTTP Supported
            self.update_progress(
                job,
                {
                    "progress": math.ceil(3 / num_checks * 99),
                    "current_status": "Checking if HTTP is supported...",
                },
            )
            check_record.http_supported = self.check_supports_http(url)
            logger.debug(f"{check_record.http_supported=}")

            # HTTPS Supported
            self.update_progress(
                job,
                {
                    "progress": math.ceil(4 / num_checks * 99),
                    "current_status": "Checking if HTTPS is supported...",
                },
            )
            check_record.https_supported = self.check_supports_https(url)
            logger.debug(f"{check_record.https_supported=}")

            # Admin Site
            self.update_progress(
                job,
                {
                    "progress": math.ceil(5 / num_checks * 99),
                    "current_status": "Checking for admin site...",
                },
            )
            (
                check_record.admin_found,
                check_record.admin_forces_https,
            ) = self.check_admin(url)
            logger.debug(f"{check_record.admin_found=}")
            logger.debug(f"{check_record.admin_forces_https=}")

            # Login Page
            self.update_progress(
                job,
                {
                    "progress": math.ceil(6 / num_checks * 99),
                    "current_status": "Checking for login page...",
                },
            )
            (
                check_record.login_found,
                check_record.login_forces_https,
            ) = self.check_login(url)
            logger.debug(f"{check_record.login_found=}")
            logger.debug(f"{check_record.login_forces_https=}")

            # Trace Method
            self.update_progress(
                job,
                {
                    "progress": math.ceil(7 / num_checks * 99),
                    "current_status": "Checking for TRACE method...",
                },
            )
            check_record.trace_allowed = self.check_trace(url)
            logger.debug(f"{check_record.trace_allowed=}")

            # Debug enabled
            self.update_progress(
                job,
                {
                    "progress": math.ceil(8 / num_checks * 99),
                    "current_status": "Checking if DEBUG is enabled...",
                },
            )
            check_record.debug_enabled = self.check_runs_debug(url)
            logger.debug(f"{check_record.debug_enabled=}")

            # CSRF Cookie
            self.update_progress(
                job,
                {
                    "progress": math.ceil(9 / num_checks * 99),
                    "current_status": "Checking CSRF cookie...",
                },
            )
            check_record.csrf_cookie_found = True if self.find_csrf_cookie() else False
            logger.debug(f"{check_record.csrf_cookie_found=}")

            # Session Cookie
            self.update_progress(
                job,
                {
                    "progress": math.ceil(10 / num_checks * 99),
                    "current_status": "Checking session cookies...",
                },
            )
            session_cookie = self.find_session_cookie()
            if session_cookie:
                check_record.session_cookie_found = True
                check_record.session_cookie_secure = session_cookie.secure
                check_record.session_cookie_httponly = session_cookie.has_nonstandard_attr(  # noqa
                    "httponly"
                )
            else:
                check_record.session_cookie_found = False
            logger.debug(f"{check_record.session_cookie_found=}")
            logger.debug(f"{check_record.session_cookie_secure=}")
            logger.debug(f"{check_record.session_cookie_httponly=}")

            # Checks completed
            self.update_progress(
                job,
                {
                    "progress": math.ceil(11 / num_checks * 99),
                    "current_status": "Checks completed saving details...",
                },
            )
            check_record.update_recommendation_count()
            check_record.save()

            # Checks completed
            self.update_progress(
                job,
                {
                    "progress": 100,
                    "current_status": "Completed!",
                    "check_id": str(check_record.id),
                },
            )
            logger.debug(f"{str(check_record.id)=}")
            logger.debug(f"{type(check_record.id)=}")
            return check_record
        except Exception as error:
            return error

    def check_supports_http(self, url):
        try:
            logger.debug(
                f"Starting check_supports_http - {url.replace('https:', 'http:')}"
            )
            response = self.session.get(url.replace("https:", "http:"), timeout=7)
        except Exception:
            # We return None if the website is not accessible with HTTP - this will be
            # a recommendation to the user.
            return None

        scheme = urlparse(response.url).scheme
        logger.debug(f"check_supports_http: {scheme=}")

        if scheme == "http":
            # This means we did not get redirected to an HTTPS site, so we return False
            # which results in an warning for the user.
            return False

        if urlparse(response.url).scheme == "https":
            # This returns True in the event that the scheme redirected from HTTP.
            return True

        return None

    def check_supports_https(self, url):
        try:
            logger.debug(
                f"Starting check_supports_https - {url.replace('http:', 'https:')}"
            )
            response = self.session.get(url.replace("http:", "https:"), timeout=7)
        except Exception:
            # Returns False if the site is not accessible over HTTPS
            return False

        # Returns true if we can access the site over HTTPS with a good status_code
        if response.status_code == 200:
            return True
        else:
            return False

    def check_supports_hsts(self, url):
        try:
            ssltest = self.session.get(url.replace("http:", "https:"), timeout=7)
        except Exception:
            return False
        return "Strict-Transport-Security" in ssltest.headers

    def check_runs_debug(self, url):
        data = self.session.get(
            urljoin(url, "[][][][][]-this-tries-to-trigger-404...."), timeout=7
        )
        return (
            "You're seeing this error because you have <code>DEBUG = True</code>"
            in data.content.decode()
        )

    def check_trace(self, url):
        response = self.session.request("TRACE", url, timeout=7)
        return (
            "Content-Type" in response.headers
            and response.headers["Content-Type"] == "message/http"
        )

    def check_admin(self, url):
        response = self.session.get(urljoin(url, "admin"), timeout=7)
        if response.status_code == 404:
            return (False, None)
        data = response.content.lower().decode()
        admin_found = '"id_password"' in data and (
            "csrfmiddlewaretoken" in data
            or "Django" in data
            or "__admin_media_prefix__" in data
        )
        return (admin_found, self._response_used_https(response))

    def check_login(self, url):
        response = self.session.get(urljoin(url, "accounts/login"), timeout=7)
        if response.status_code == 404:
            response = self.session.get(urljoin(url, "login"), timeout=7)
            if response.status_code == 404:
                return (False, None)
        return (True, self._response_used_https(response))

    def _response_used_https(self, response):
        logger.debug(f"_response_used_https: {response.url[:5]=}")
        return response.url[:5] == "https"

    def find_session_cookie(self):
        for cookie in self.session.cookies:
            if cookie.name == "sessionid":
                return cookie
        return False

    def find_csrf_cookie(self):
        for cookie in self.session.cookies:
            if cookie.name == "csrftoken":
                return cookie
        return False

    def update_progress(self, job, dict_updates):
        job.meta.update(dict_updates)
        job.save_meta()
