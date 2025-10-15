from django.urls import path
from .views import FeedbackHistoryView, FeedbackContentView, ProgressHistoryView, ProgressContentView, FeedbackDetailsView, SpecificFeedbackView, ProgressDetailsView, SpecificProgressView

urlpatterns = [
    path('feedback_history/', FeedbackHistoryView.as_view(), name="feedbackHistory"),
    path('feedback_data/<int:feedback_id>/', FeedbackContentView.as_view(), name="feedbackData"),
    path('progress_history/', ProgressHistoryView.as_view(), name="progressHistory"),
    path('progress_data/<int:progress_id>/', ProgressContentView.as_view(), name="progressData"),
    path('details/', FeedbackDetailsView.as_view(), name='feedback_details'),
    path("specific/details/", SpecificFeedbackView.as_view(), name="specific-feedback-details"),
    path('progress/details/', ProgressDetailsView.as_view(), name='progress_details'),
    path("specific/progress/details/", SpecificProgressView.as_view(), name="specific-progress-details"),


]
