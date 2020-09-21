import logging

from django.views.generic import FormView
from django.urls import reverse_lazy

from checks.forms import URLSubmitForm

logger = logging.getLogger(__name__)


class HomePageView(FormView):
    template_name = "website/home.html"
    form_class = URLSubmitForm
    success_url = reverse_lazy("checks:results")


class AboutPageView(FormView):
    template_name = "website/about.html"
    form_class = URLSubmitForm
    success_url = reverse_lazy("checks:results")
