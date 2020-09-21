from django.urls import path

from .views import ResultsView, ChecksView, CheckStatusView

app_name = "checks"
urlpatterns = [
    path("", ChecksView.as_view(), name="check"),
    path("<str:pk>/", ResultsView.as_view(), name="result"),
    path(
        "check_status/<str:job_id>",
        CheckStatusView.as_view(),
        name="check_status",
    ),
]
