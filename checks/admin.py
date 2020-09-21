from django.contrib import admin

from .models import Check


class CheckAdmin(admin.ModelAdmin):
    list_display = ("url", "created_at", "updated_at")
    ordering = ("created_at",)


admin.site.register(Check, CheckAdmin)
