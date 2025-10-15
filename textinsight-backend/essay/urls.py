from django.urls import path
from .views import ManageEssayView, SubmitEssayView, SubmissionHistoryView, SubmissionContentView, NotificationHistoryView, DashboardView, CreateAssignment, TeacherAssignmentsView, StudentsSubmissionView,SpecificStudentSubmissionView, TeacherDashboardView, AssignmentDetailsView

urlpatterns = [
    path('manage_essay/', ManageEssayView.as_view(), name="manageEssay"),
    path('submit_essay/', SubmitEssayView.as_view(), name="submitEssay"),
    path('submission_history/', SubmissionHistoryView.as_view(), name="submissionHistory"),
    path('submission_content/<int:submission_id>/', SubmissionContentView.as_view(), name="submissionContent"),
    path('notification_history/', NotificationHistoryView.as_view(), name="notificationHistory"),
    path('dashboard/', DashboardView.as_view(), name="Dashboard"),
    path('create_assignment/', CreateAssignment.as_view(), name="createAssignment"),
    path('update_assignment/', CreateAssignment.as_view(), name="updateAssignment"),
    path('teacher-assignment/', TeacherAssignmentsView.as_view(), name="teacherAssignment"),
    path('assignment-submission/<int:assignment_id>/', StudentsSubmissionView.as_view(), name="StudentsSubmission"),
    path("submissions/specific/", SpecificStudentSubmissionView.as_view(), name="specific_submission"),
    path('teacher-dashboard/', TeacherDashboardView.as_view(), name="teacher-dashboard"),
    path('assignment-details/<int:assignment_id>/', AssignmentDetailsView.as_view(), name="assignmentDetails")
]