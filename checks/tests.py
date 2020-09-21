from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains

client = Client()


def test_checkspage_status(client):
    response = client.get(reverse("checks:check"))
    assert response.status_code == 200


def test_checkspage_template(client):
    response = client.get(reverse("checks:check"))
    assertTemplateUsed(response, "checks/check.html")


def test_checkspage_content(client):
    response = client.get(reverse("checks:check"))
    assertContains(response, "Run a checkup on my site")
