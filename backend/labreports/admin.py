from django.contrib import admin
from .models import LabReport


@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ("id", "experiment_name", "subject", "language", "short_extracted_output", "created_at")
    search_fields = ("experiment_name", "subject", "language", "extracted_output")
    list_filter = ("subject", "language", "created_at")

    def short_extracted_output(self, obj):
        return obj.extracted_output[:80]

    short_extracted_output.short_description = "Extracted Output"