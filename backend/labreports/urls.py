from django.urls import path
from .views import GenerateLabRecordView, GenerateLabRecordFromImageView

urlpatterns = [
    path("generate/", GenerateLabRecordView.as_view(), name="generate-lab-record"),
    path("generate-from-image/", GenerateLabRecordFromImageView.as_view(), name="generate-lab-record-from-image"),
]