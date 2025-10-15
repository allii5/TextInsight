import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from decorators.role_based_decorator import role_required
from django.utils.decorators import method_decorator
from feedback.service import FeedbackService
from dto.response.success_response_dto import SuccessResponseDTO
from dto.response.failure_response_dto import FailureResponseDTO
from feedback.serializers import FeedbackContentRequestSerializer, ProgressContentRequestSerializer, AssignmentQuerySerializer, FeedbackQuerySerializer, ProgressQuerySerializer


logging.basicConfig(level=logging.ERROR)

class FeedbackHistoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the feedback history for the authenticated student
    @method_decorator(role_required('student'))
    def get(self, request):
        try:
            data = FeedbackService().get_feedback_history(request.user.id)
            return Response(SuccessResponseDTO("Fetch The Feedback History", 200, data).to_json())
        except Exception as e:
            logging.error("An error occurred in feedback_history %s", str(e), exc_info=True)
            return Response(FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(), status=500)

class FeedbackContentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the content of a specific feedback
    @method_decorator(role_required('student'))
    def get(self, request, feedback_id):
        # Validate the feedback_id using the serializer
        serializer = FeedbackContentRequestSerializer(data={'feedback_id': feedback_id})
        
        if not serializer.is_valid():
            # Respond with validation errors if data is invalid
            return Response(
                FailureResponseDTO("Invalid data", 400, serializer.errors).to_json(), 
                status=400
            )

        try:
            # Access the validated data
            feedback_id = serializer.validated_data['feedback_id']

            # Call the service to get feedback content
            data = FeedbackService().get_feedback(request.user.id, feedback_id)
            if data:
                return Response(
                    SuccessResponseDTO("Fetch The Feedback Content", 200, data).to_json()
                )
            
            # Handle case where feedback does not exist
            return Response(
                FailureResponseDTO("Student does not have feedback of this ID", 500).to_json(),
                status=500
            )

        except Exception as e:
            # Log the exception and respond with a failure message
            logging.error("An error occurred in feedback_content %s", str(e), exc_info=True)
            return Response(
                FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(),
                status=500
            )

class ProgressHistoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the progress history for the authenticated student
    @method_decorator(role_required('student'))
    def get(self, request):
        try:
            data = FeedbackService().get_progress_history(request.user.id)
            return Response(SuccessResponseDTO("Fetch The Progress History", 200, data).to_json())
        except Exception as e:
            logging.error("An error occurred in progress_history %s", str(e), exc_info=True)
            return Response(FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(), status=500)

class ProgressContentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the content of a specific progress
    @method_decorator(role_required('student'))
    def get(self, request, progress_id):
        # Validate the progress_id using the serializer
        serializer = ProgressContentRequestSerializer(data={'progress_id': progress_id})

        if not serializer.is_valid():
            # Respond with validation errors if data is invalid
            return Response(
                FailureResponseDTO("Invalid data", 400, serializer.errors).to_json(),
                status=400
            )

        try:
            # Access the validated data
            progress_id = serializer.validated_data['progress_id']

            # Call the service to get progress content
            data = FeedbackService().get_progress(request.user.id, progress_id)
            if data:
                return Response(
                    SuccessResponseDTO("Fetch The Progress Content", 200, data).to_json()
                )
            
            # Handle case where progress does not exist
            return Response(
                FailureResponseDTO("Student does not have a progress report of this ID", 500).to_json(),
                status=500
            )

        except Exception as e:
            # Log the exception and respond with a failure message
            logging.error("An error occurred in progress_content %s", str(e), exc_info=True)
            return Response(
                FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(),
                status=500
            )


class FeedbackDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the feedback history for the authenticated teacher
    @method_decorator(role_required('teacher'))
    def get(self, request):
        """
        Fetch feedback details for students of a specific assignment using `assignment_id` as a query parameter.
        """
        # Step 1: Validate query parameters with the serializer
        serializer = AssignmentQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Extract validated assignment_id
        assignment_id = serializer.validated_data['assignment_id']

        # Step 3: Initialize repositories and service
        feedback_service = FeedbackService()

        # Step 4: Fetch feedback details
        try:
            feedback_details = feedback_service.fetch_feedback_details(assignment_id)
            # if not feedback_details:
            #    return Response(
            #        {"message": "No feedback found for the given assignment_id."},
            #        status=status.HTTP_404_NOT_FOUND
            #    )
            return Response({"feedback_details": feedback_details}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SpecificFeedbackView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the feedback history for the authenticated teacher
    @method_decorator(role_required('teacher'))
    def get(self, request):
        """
        Fetch specific feedback data for a student and feedback ID via query parameters.
        """
        # Step 1: Validate query parameters with serializer
        serializer = FeedbackQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Extract validated query parameters
        feedback_id = serializer.validated_data["feedback_id"]
        student_id = serializer.validated_data["student_id"]

        # Step 3: Initialize  service
        feedback_service = FeedbackService()

        # Step 4: Fetch feedback details
        try:
            feedback_details = feedback_service.get_feedback_details(student_id, feedback_id)
            # if not feedback_details:
            #     return Response(
            #         {"message": "No feedback found for the given feedback_id and student_id."},
            #         status=status.HTTP_404_NOT_FOUND
            #     )
            return Response({"feedback_details": feedback_details}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ProgressDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the progress history for the authenticated teacher
    @method_decorator(role_required('teacher'))
    def get(self, request):
        """
        Fetch progress details for students of a specific assignment using `assignment_id` as a query parameter.
        """
        # Step 1: Validate query parameters with the serializer
        serializer = AssignmentQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Extract validated assignment_id
        assignment_id = serializer.validated_data['assignment_id']

        # Step 3: Initialize repositories and service
        progress_service = FeedbackService()

        # Step 4: Fetch progress details
        try:
            progress_details = progress_service.fetch_progress_details(assignment_id)
            # if not progress_details:
            #     return Response(
            #         {"message": "No progress found for the given assignment_id."},
            #         status=status.HTTP_404_NOT_FOUND
            #     )
            return Response({"progress_details": progress_details}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class SpecificProgressView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the progress history for the authenticated teacher
    @method_decorator(role_required('teacher'))
    def get(self, request):
        """
        Fetch specific progress data for a student and progress ID via query parameters.
        """
        # Step 1: Validate query parameters with serializer
        serializer = ProgressQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Extract validated query parameters
        progress_id = serializer.validated_data["progress_id"]
        student_id = serializer.validated_data["student_id"]

        # Step 3: Initialize  service
        progress_service = FeedbackService()

        # Step 4: Fetch progress details
        try:
            progress_details = progress_service.get_progress_details(student_id, progress_id)
            if not progress_details:
                return Response(
                    {"message": "No progress found for the given progress_id and student_id."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response({"progress_details": progress_details}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)