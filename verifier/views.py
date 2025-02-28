from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import pytesseract
import PyPDF2
import os
from django.conf import settings
from .serializers import SSCMarksheetSerializer
from .serializers import CETMarksheetSerializer
import difflib


def extract_text(file_path):
    if file_path.endswith(('.jpg', '.png')):
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    elif file_path.endswith('.pdf'):
        text = ''
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ''
        return text
    return ''


class SSCMarksheetVerification(APIView):
    def post(self, request):
        serializer = SSCMarksheetSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            roll_no = serializer.validated_data['roll_no']
            result = serializer.validated_data['result']
            document_file = request.FILES['document_file']

            # Save File
            file_path = os.path.join(settings.MEDIA_ROOT, document_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in document_file.chunks():
                    destination.write(chunk)

            # Extract Text
            extracted_text = extract_text(file_path).lower()

            # Verification
            results = {
                "name_check": "Match" if name.lower() in extracted_text else "Does not match",
                "roll_no_check": "Match" if roll_no.lower() in extracted_text else "Does not match",
                "result_check": "Match" if result.lower() in extracted_text else "Does not match"
            }

            # Suggest Closest Match for Result
            if results['result_check'] == "Does not match":
                closest_match = difflib.get_close_matches(result.lower(), extracted_text.split(), n=1)
                results['nearest_result'] = closest_match[0] if closest_match else "No suggestions available."

            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CETMarksheetVerification(APIView):
    def post(self, request):
        serializer = CETMarksheetSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            roll_no = serializer.validated_data['roll_no']
            application_no = serializer.validated_data['application_no']
            category = serializer.validated_data['application_no']
            mothers_name = serializer.validated_data['application_no']
            document_file = request.FILES['document_file']

            # Save File
            file_path = os.path.join(settings.MEDIA_ROOT, document_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in document_file.chunks():
                    destination.write(chunk)

            # Extract Text
            extracted_text = extract_text(file_path).lower()

            # Verification
            results = {
                "name_check": "Match" if name.lower() in extracted_text else "Does not match",
                "roll_no_check": "Match" if roll_no.lower() in extracted_text else "Does not match",
                "application_no_check": "Match" if application_no.lower() in extracted_text else "Does not match",
                "category_check": "Match" if category.lower() in extracted_text else "Does not match",
                "mothers_name_check": "Match" if mothers_name.lower() in extracted_text else "Does not match"
            }

            # Suggest Closest Match for Result
            # if results['result_check'] == "Does not match":
            #     closest_match = difflib.get_close_matches(category.lower(), extracted_text.split(), n=1)
            #     results['nearest_result'] = closest_match[0] if closest_match else "No suggestions available."

            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
