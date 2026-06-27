import os
from django.conf import settings
from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .services.ollama_service import generate_lab_record
from .services.ocr_service import extract_text_from_image


class GenerateLabRecordView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        experiment_name = request.data.get("experiment_name", "")
        subject = request.data.get("subject", "")
        language = request.data.get("language", "")
        output_text = request.data.get("output_text", "")
        code_text = request.data.get("code_text", "")

        if not experiment_name or not subject:
            return Response(
                {"error": "experiment_name and subject are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lab_record = generate_lab_record(
                experiment_name=experiment_name,
                subject=subject,
                language=language,
                output_text=output_text,
                code_text=code_text
            )

            return Response(
                {
                    "message": "Lab record generated successfully",
                    "experiment_name": experiment_name,
                    "subject": subject,
                    "language": language,
                    "lab_record": lab_record
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateLabRecordFromImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        experiment_name = request.data.get("experiment_name", "")
        subject = request.data.get("subject", "")
        language = request.data.get("language", "")
        code_text = request.data.get("code_text", "")
        image = request.FILES.get("image")

        if not experiment_name or not subject:
            return Response(
                {"error": "experiment_name and subject are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not image:
            return Response(
                {"error": "image file is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            saved_path = default_storage.save(f"uploads/{image.name}", image)
            absolute_image_path = os.path.join(settings.MEDIA_ROOT, saved_path)

            extracted_output = extract_text_from_image(absolute_image_path)

            lab_record = generate_lab_record(
                experiment_name=experiment_name,
                subject=subject,
                language=language,
                output_text=extracted_output,
                code_text=code_text
            )

            image_url = request.build_absolute_uri(settings.MEDIA_URL + saved_path)

            return Response(
                {
                    "message": "Lab record generated from image successfully",
                    "experiment_name": experiment_name,
                    "subject": subject,
                    "language": language,
                    "image_url": image_url,
                    "extracted_output": extracted_output,
                    "lab_record": lab_record
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
