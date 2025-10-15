import csv
from io import StringIO
import os
from django.http import HttpResponse
from authentication.services import StudentAccountService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from decorators.role_based_decorator import role_required
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated, AllowAny

from textinsight import settings
from .serializers import (
    SignupTeacherSerializer, LoginSerializer, ResetPasswordSerializer,
    CreateStudentSerializer, FirstTimeLoginSerializer, ForgotPasswordSerializer,
    ChangePasswordSerializer, StudentAccountsSerializer
)
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .permissions import IsTeacher, IsStudent
import logging

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class SignupTeacherView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignupTeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Teacher account created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Step 1: Parse and validate credentials
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        # Step 2: Check if it's the first-time login
        if user.first_time_login:  # Check if first time login
            user.send_verification_email(action="create_account")  # Send verification email
            return Response({"message": "Verification email sent. Please verify your email to complete the login."}, status=200)
        
        # Step 3: If user is verified, create a token (JWT) for the authenticated user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Step 4: Return token and additional user details
        return Response({
            "message": "Login successful",
            "role": user.role,
            "username": user.username,
            "access_token": access_token,
            "refresh_token": str(refresh)
        }, status=200)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")
        action = request.GET.get("action")  # Extract action parameter
        try:
            if not uid or not token or not action:
                return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

            # Decode UID and get the user
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)

            # Validate the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            # Handle actions
            if action == "create_account":
                user.status = "verified"
                user.first_time_login = False
                user.save()
                return Response({"message": "Account successfully verified"}, status=status.HTTP_200_OK)

            elif action == "reset_password":
                # For password reset, simply return success. Password will be updated on another endpoint.
                return Response({"message": "Token verified. Proceed to reset your password."}, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Invalid action parameter"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            logger.error("User not found for UID: %s", uid)
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("An unexpected error occurred: %s", str(e))
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# class ResetPasswordView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         #user.send_verification_email(action="create_account")  # Send verification email

#         serializer = ResetPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            user.send_verification_email(action="reset_password")
            return Response({"message": "Password reset email sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateStudentView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        # Deserialize the incoming data
        serializer = CreateStudentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create the student and return the user instance
            student = serializer.save()

            return Response({"message": "Student account created and email sent"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateStudentsAccounts(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        self.account_service = StudentAccountService()
    
    @method_decorator(role_required('teacher'))
    def post(self, request):
        """
        Validates input, creates student accounts, and generates downloadable CSV with usernames.
        """
        # Step 1: Validate the data using the DRF serializer
        serializer = StudentAccountsSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Handle account creation using the service layer
        try:
            # Get the valid emails from the serializer's validated data
            valid_emails = serializer.valid_emails
            number_of_accounts = serializer.validated_data['number_of_accounts']
            
            response = self.account_service.handle_bulk_account_creation(
                valid_emails=valid_emails,
                number_of_accounts=number_of_accounts,
                teacher_email=request.user.email
            )
            
            if response['status'] == 'error':
                return Response({'error': response['message'], 'details': response.get('details', '')}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Step 3: Generate CSV file with created usernames
            created_accounts = response.get('created_accounts', [])
            if created_accounts:
                return self._generate_csv_response(created_accounts)

            return Response({'message': 'No accounts were created.'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({'error': 'An unexpected error occurred.', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_csv_response(self, accounts):
        """
        Generates a CSV file containing usernames and triggers download.
        """
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        
        # Write header
        csv_writer.writerow(['Username'])
        
        # Write each username
        for account in accounts:
            csv_writer.writerow([account['username']])
        
        # Prepare response
        response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="created_student_accounts.csv"'
        return response

class DownloadSampleCSV(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'samples', 'sample_student_emails.csv')
        
        try:
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="sample_student_emails.csv"'
                return response
        except FileNotFoundError:
            return Response(
                {'error': 'Sample file not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        action = request.data.get('action')  # "create_account" or "reset_password"

        if not username or not action:
            return Response({"error": "Missing required parameters: email or action"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the user by email
            user = User.objects.get(username=username)
            
            # Verify the action type
            if action == "create_account":
                if user.status == "verified":
                    return Response({"message": "Account is already verified."}, status=status.HTTP_400_BAD_REQUEST)
                # Send the verification email for account creation
                user.send_verification_email(action="create_account")
                return Response({"message": "Verification email resent. Please verify your email to complete the registration."}, status=status.HTTP_200_OK)
            
            elif action == "reset_password":
                # Send the verification email for password reset
                user.send_verification_email(action="reset_password")
                return Response({"message": "Password reset email resent. Please check your inbox."}, status=status.HTTP_200_OK)
            
            else:
                return Response({"error": "Invalid action. Choose either 'create_account' or 'reset_password'."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            logger.error("User not found for username: %s", username)
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("An error occurred: %s", str(e))
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)