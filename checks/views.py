import logging

from django.views.generic import FormView, View, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse

import django_rq

from .forms import URLSubmitForm
from .models import Check
from .checker import SecurityChecker

logger = logging.getLogger(__name__)


class ChecksView(FormView):
    """
    This view receives the post data from the form and shows the progress bar. If this
    page is accessed with a GET request it will show the form to submit a URL.
    Once processing is complete it will show a link to the results page with the UUID
    of the URL that was submitted.
    """

    template_name = "checks/check.html"
    form_class = URLSubmitForm
    # success_url = reverse_lazy("checks:results")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            context = self.get_context_data()
            job = self.start_job(form.cleaned_data)
            context["job_id"] = job.id
            return self.render_to_response(context)

    def start_job(self, valid_data):
        """
        This receives valid data from the form and starts the job using the
        SecurityChecker class and the run_job method.
        """
        checker = SecurityChecker()
        queue = django_rq.get_queue("checks")
        return queue.enqueue(checker.run_check, url=valid_data["url"])
        # return checker.run_check().delay(valid_data["url"])


class ResultsView(DetailView):
    template_name = "checks/result.html"
    model = Check


class CheckStatusView(View):
    def get(self, request, job_id):

        job = django_rq.get_queue("checks").fetch_job(job_id)

        response = {
            "status": "invalid",
            "current_status": "",
            "progress": "",
        }

        if job:
            response = {
                "status": job.get_status(),
                "current_status": job.meta.get("current_status", ""),
                "progress": job.meta.get("progress", ""),
                "check_id": job.meta.get("check_id", ""),
            }

        if response["check_id"]:
            response["check_url"] = reverse_lazy(
                "checks:result", args=[response["check_id"]]
            )

        return JsonResponse(response)
