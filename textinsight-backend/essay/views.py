import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from decorators.role_based_decorator import role_required
from django.utils.decorators import method_decorator
from essay.service import EssayService
from essay.service import AssignmentService
from dto.response.success_response_dto import SuccessResponseDTO
from dto.response.failure_response_dto import FailureResponseDTO
from essay.serializers import SubmissionContentRequestSerializer, EssaySubmissionSerializer, AssignmentIdSerializer, AssignmentStudentSerializer, CreateAssignmentSerializer, UpdateAssignmentSerializer
from rest_framework import status
from custom_error_classes import AssignmentNotFoundError, DueDatePassedError, FeedbackNotAvailableError, UserNotInClassError, SubmissionLimitExceededError



logging.basicConfig(level=logging.ERROR)

class ManageEssayView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the list of pending assignments for the authenticated student
    @method_decorator(role_required('student'))
    def get(self, request):
        try:
            print(request.user)
            data = EssayService().fetchListOfPendingAssignment(request.user.id)
            return Response(SuccessResponseDTO("Fetch The Pending Assignments", 200, data).to_json())
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return Response(FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(), status=500)

class SubmitEssayView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('student'))
    def post(self, request):
        # Parse and validate the request body using EssaySubmissionSerializer
        try:
            body = json.loads(request.body)
            print(body)
        except json.JSONDecodeError:
            return Response(FailureResponseDTO("Invalid JSON data", 400).to_json(), status=400)

        serializer = EssaySubmissionSerializer(data=body)

        if not serializer.is_valid():
            # Respond with validation errors if the data is invalid
            return Response(
                FailureResponseDTO("Invalid data", 400, serializer.errors).to_json(),
                status=400
            )

        # Extract validated data
        validated_data = serializer.validated_data
        assignment_id = validated_data['assignment_id']
        introduction = validated_data['introduction']
        middle = validated_data['middle']
        conclusion = validated_data['conclusion']

        try:
            # Process the essay submission
            data = EssayService().submitEssay(request.user, assignment_id, introduction, middle, conclusion)
            return Response(
                SuccessResponseDTO("Essay processed successfully", 200, data).to_json(),
                status=200
            )

        # Handle known exceptions
        except AssignmentNotFoundError as e:
            return Response(FailureResponseDTO(str(e), 404).to_json(), status=404)
        except DueDatePassedError as e:
            return Response(FailureResponseDTO(str(e), 400).to_json(), status=400)
        except UserNotInClassError as e:
            return Response(FailureResponseDTO(str(e), 403).to_json(), status=403)
        except FeedbackNotAvailableError as e:
            return Response(FailureResponseDTO(str(e), 400).to_json(), status=400)
        except SubmissionLimitExceededError as e:
            return Response(FailureResponseDTO(str(e), 400).to_json(), status=400)

        # Handle unexpected errors
        except Exception as e:
            logging.error("An unexpected error occurred in submit_essay view: %s", str(e), exc_info=True)
            return Response(
                FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(),
                status=500
            )
class SubmissionHistoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the submission history for the authenticated student
    @method_decorator(role_required('student'))
    def get(self, request):
        try:
            data = EssayService().get_submission_history(request.user.id)
            return Response(SuccessResponseDTO("Fetch The Submission History", 200, data).to_json())
        except Exception as e:
            logging.error("An error occurred in submission_history %s", str(e), exc_info=True)
            return Response(FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(), status=500)

class SubmissionContentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the content of a specific submission for the authenticated student
    @method_decorator(role_required('student'))
    def get(self, request, submission_id):
        # Validate submission_id using the serializer
        serializer = SubmissionContentRequestSerializer(data={'submission_id': submission_id})

        if not serializer.is_valid():
            # Respond with validation errors if the data is invalid
            return Response(
                FailureResponseDTO("Invalid data", 400, serializer.errors).to_json(),
                status=400
            )

        try:
            # Access the validated data
            submission_id = serializer.validated_data['submission_id']

            # Call the service to fetch submission content
            data = EssayService().get_submission_content(request.user.id, submission_id)
            if data:
                return Response(
                    SuccessResponseDTO("Fetch The Submission Content", 200, data).to_json()
                )
            
            # Handle case where submission does not exist
            return Response(
                FailureResponseDTO("Student does not have a submission with this ID.", 500).to_json(),
                status=500
            )

        except Exception as e:
            # Log the exception and respond with a failure message
            logging.error("An error occurred in submission_content %s", str(e), exc_info=True)
            return Response(
                FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(),
                status=500
            )

class NotificationHistoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the notification history for the authenticated student
    @method_decorator(role_required('student'))
    def get(self, request):
        try:
            data = EssayService().get_notification_history(request.user.id)
            return Response(SuccessResponseDTO("Fetch The Notification History", 200, data).to_json())
        except Exception as e:
            logging.error("An error occurred in notification_history %s", str(e), exc_info=True)
            return Response(FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(), status=500)

class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the dashboard data for the authenticated student
    @method_decorator(role_required('student'))
    def get(self, request):
        try:
            data = EssayService().dashboardData(request.user.id)
            response_data = {
                "name": request.user.name,
                "dashboard": data
            }
            return Response(SuccessResponseDTO("Fetch The Dashboard Data", 200, response_data).to_json())
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return Response(FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(), status=500)


class CreateAssignment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.assignment_service = AssignmentService()

    @method_decorator(role_required('teacher'))
    def post(self, request):
        # Use CreateAssignmentSerializer for validation
        serializer = CreateAssignmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Pass validated data to the service
        response = self.assignment_service.create_assignment(
            teacher_id=request.user.id,
            data=serializer.validated_data
        )

        if response['status'] == 'success':
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': response.get('errors', response.get('message'))}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(role_required('teacher'))
    def put(self, request):
        # Use UpdateAssignmentSerializer for validation
        serializer = UpdateAssignmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Pass validated data to the service
        response = self.assignment_service.update_assignment(
            teacher_id=request.user.id,
            data=serializer.validated_data
        )

        if response['status'] == 'success':
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'errors': response.get('errors', response.get('message'))}, status=status.HTTP_400_BAD_REQUEST)

class TeacherAssignmentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def get(self, request):
        teacher_id = request.user.id  

        service = AssignmentService()
        assignments = service.get_teacher_assignments(teacher_id)

        return Response({
            "data": assignments,
            "message": "No assignments found." if not assignments else "Assignments retrieved successfully."
        }, status=status.HTTP_200_OK)

class StudentsSubmissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def get(self, request, assignment_id):
        """
        Fetches the list of students who submitted essays for the given assignment.
        Returns:
            JSON response with student ID, name, and submission date.
        """

        serializer = AssignmentIdSerializer(data={"assignment_id": assignment_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        essay_service = EssayService()

        try:
            submissions = essay_service.fetch_students_submission_data(assignment_id)
            return Response({"submissions": submissions}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpecificStudentSubmissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def get(self, request):
        """
        Fetch specific submission content for a student in an assignment.
        """
        # Parse query parameters
        data = {
            "submission_id": request.query_params.get("submission_id"),
            "student_id": request.query_params.get("student_id"),
        }

        # Validate data
        serializer = AssignmentStudentSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        submission_id = serializer.validated_data["submission_id"]
        student_id = serializer.validated_data["student_id"]

        # Initialize repository and service
        essay_service = EssayService()

        try:
            # Fetch submission content
            content = essay_service.fetch_student_submission_content(student_id, submission_id)
            return Response({"submission": content}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TeacherDashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Fetches the dashboard data for the authenticated student
    @method_decorator(role_required('teacher'))
    def get(self, request):
        try:
            data = EssayService().get_teacher_dashboard(request.user.id)
            response_data = {
                "name": request.user.name,
                "dashboard": data
            }
            return Response({"message" : "Fetch The Dashboard Data", "data" : response_data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return Response(FailureResponseDTO("An unexpected error occurred", 500, str(e)).to_json(), status=500)
        
class AssignmentDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required('teacher'))
    def get(self, request, assignment_id):
        try:
            data = AssignmentService().get_assignment_details(assignment_id)
            return Response(SuccessResponseDTO("Fetch The Assignment Details", 200, data).to_json())
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)