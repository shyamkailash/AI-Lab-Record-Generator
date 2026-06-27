from django.db import models


class LabReport(models.Model):
    experiment_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    language = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    extracted_output = models.TextField(blank=True)
    lab_record = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.experiment_name
