from django.urls import path
from .views import (
    SignupTeacherView, LoginView, VerifyEmailView, CreateStudentsAccounts, DownloadSampleCSV,
    ResetPasswordView, CreateStudentView, CustomTokenObtainPairView,
    ForgotPasswordView, ChangePasswordView, ResendVerificationEmailView
)

urlpatterns = [
    path('api/signup-teacher/', SignupTeacherView.as_view(), name='signup_teacher'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/create-student-accounts/', CreateStudentsAccounts.as_view(), name='create_students_accounts'),
    path('api/download-sample-csv/', DownloadSampleCSV.as_view(), name='download_sample_csv'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('api/create-student/', CreateStudentView.as_view(), name='create_student'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('api/change-password/', ChangePasswordView.as_view(), name="change_password"),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(), name='resend_verification_email'),
]
