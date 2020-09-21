# Generated by Django 3.1.1 on 2020-09-21 09:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Check",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("url", models.URLField()),
                ("no_of_recommendations", models.IntegerField(default=0)),
                ("debug_enabled", models.BooleanField()),
                ("http_supported", models.BooleanField(null=True)),
                ("https_supported", models.BooleanField()),
                ("hsts_header_found", models.BooleanField()),
                ("xframe_header_found", models.BooleanField()),
                ("admin_found", models.BooleanField()),
                ("admin_forces_https", models.BooleanField(null=True)),
                ("login_found", models.BooleanField()),
                ("login_forces_https", models.BooleanField(null=True)),
                ("trace_allowed", models.BooleanField()),
                ("csrf_cookie_found", models.BooleanField()),
                ("session_cookie_found", models.BooleanField()),
                ("session_cookie_secure", models.BooleanField(null=True)),
                ("session_cookie_httponly", models.BooleanField(null=True)),
            ],
        ),
    ]