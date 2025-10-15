import os
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from classes.services import ClassService
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from decorators.role_based_decorator import role_required
from django.utils.decorators import method_decorator
from classes.serializers import UpdateClassSerializer, CreateClassSerializer
import logging

from textinsight import settings

logging.basicConfig(level=logging.ERROR)

class CreateClassView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def post(self, request):
        # Initialize serializer with data and files
        serializer = CreateClassSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Access validated data and usernames extracted from the CSV file
        validated_data = serializer.validated_data
        csv_usernames = serializer.csv_usernames

        # Call the service to create the class
        service = ClassService()
        result = service.create_class_with_students(
            class_name=validated_data['class_name'],
            teacher_id=request.user.id,
            selected_usernames=validated_data['selected_usernames'],
            csv_usernames=csv_usernames
        )

        if result['status'] == 'error':
            return Response({'errors': result['errors']}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'message': result['message'], 'invalid_usernames': result['invalid_usernames']},
            status=status.HTTP_201_CREATED
        )

class UpdateClassView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def post(self, request):
        teacher_id = request.user.id

        # Use the serializer to validate and process data
        serializer = UpdateClassSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        validated_data = serializer.validated_data
        service = ClassService()
        
        result = service.update_class(
            class_id=validated_data['class_id'],
            class_name=validated_data['class_name'],
            added_usernames=validated_data['added_usernames'],
            teacher_id=teacher_id
        )

        if result['status'] == 'error':
            return Response({'errors': result['errors']}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': result['message']}, status=status.HTTP_200_OK)

class FetchClassDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def get(self, request, class_id):
        """
        Fetch details of a specific class for updating.
        """
        service = ClassService()
        try:
            # Fetch the class details
            class_obj = service.class_repo.findById(class_id)
            if not class_obj:
                return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

            # Fetch students enrolled in the class
            students = service.class_students_repo.model.objects.filter(class_id=class_id)
            student_usernames = [student.student_id.username for student in students]

            # Prepare the response data
            response_data = {
                "class_id": class_obj.id,
                "class_name": class_obj.class_name,
                "current_students": student_usernames,
                "student_count": class_obj.student_count
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TeacherClassesView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def get(self, request):
        """
        Fetches classes created by a teacher.
        """
        # Ensure the teacher exists
        teacher_id = request.user.id
        
        class_service = ClassService()

        # Fetch classes
        try:
            classes = class_service.fetch_teacher_classes(teacher_id)
            return Response({"data": classes}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SearchStudentsInClassView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def get(self, request, class_id):
        """
        Search for students in a specific class.
        """
        search_query = request.query_params.get("q", None)  # Get the query parameter "q" for search.
        service = ClassService()

        try:
            # Fetch students from the service
            students = service.search_students_in_class(class_id, search_query)
            return Response({"students": students}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SearchStudentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def get(self, request):
        """
        Search for all students in the database.
        """
        search_query = request.query_params.get("q", None)  # Get the query parameter "q" for search.
        service = ClassService()

        try:
            # Fetch students from the service
            students = service.search_students(search_query)
            return Response({"students": students}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadSampleCSV(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'samples', 'sample_student_usernames.csv')
        
        try:
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="sample_student_usernames.csv"'
                return response
        except FileNotFoundError:
            return Response(
                {'error': 'Sample file not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )