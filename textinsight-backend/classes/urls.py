from django.urls import path
from .views import (
    CreateClassView, UpdateClassView, FetchClassDetailsView, TeacherClassesView, SearchStudentsInClassView, SearchStudentsView, DownloadSampleCSV
)

urlpatterns = [
    path('create-class/', CreateClassView.as_view(), name="create-class"),
    path('update-class/', UpdateClassView.as_view(), name="update-class"),
    path('fetch-classes/', TeacherClassesView.as_view(), name="fetch-clases"),
    path('<int:class_id>/details/', FetchClassDetailsView.as_view(), name='fetch-class-details'),
    path('<int:class_id>/students/search/', SearchStudentsInClassView.as_view(), name='search_students_class'),
    path('students/search/', SearchStudentsView.as_view(), name='search_students'),
    path('download-sample-csv/', DownloadSampleCSV.as_view(), name='download_sample_csv'),
]
