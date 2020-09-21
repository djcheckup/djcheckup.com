from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains

client = Client()


def test_homepage_status(client):
    response = client.get(reverse("website:home"))
    assert response.status_code == 200


def test_homepage_template(client):
    response = client.get(reverse("website:home"))
    assertTemplateUsed(response, "website/home.html")


def test_homepage_content(client):
    response = client.get(reverse("website:home"))
    assertContains(response, "Get started")


def test_aboutpage_status(client):
    response = client.get(reverse("website:about"))
    assert response.status_code == 200


def test_aboutpage_template(client):
    response = client.get(reverse("website:about"))
    assertTemplateUsed(response, "website/about.html")


def test_aboutpage_content(client):
    response = client.get(reverse("website:about"))
    assertContains(response, "About this site")
