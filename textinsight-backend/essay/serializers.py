from rest_framework import serializers
from .models import Essay, Assignment
from authentication.models import User
from datetime import datetime
from django.utils import timezone

class SubmissionContentRequestSerializer(serializers.Serializer):
    submission_id = serializers.IntegerField()

    def validate_submission_id(self, value):
        """
        Custom validation for submission_id field.
        Ensures it is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Submission ID must be a positive integer.")
        return value

class EssaySubmissionSerializer(serializers.Serializer):
    assignment_id = serializers.IntegerField(required=True, error_messages={'required': 'This field is required.'})
    introduction = serializers.CharField(required=True, error_messages={'required': 'This field is required.'})
    middle = serializers.CharField(required=True, error_messages={'required': 'This field is required.'})
    conclusion = serializers.CharField(required=True, error_messages={'required': 'This field is required.'})


class AssignmentIdSerializer(serializers.Serializer):
    assignment_id = serializers.IntegerField(required=True)

    def validate_assignment_id(self, value):
        """
        Validate that the assignment ID exists in the database.
        """
        if not Assignment.objects.filter(id=value).exists():
            raise serializers.ValidationError("The provided assignment ID is invalid or does not exist.")
        return value

class AssignmentStudentSerializer(serializers.Serializer):
    submission_id = serializers.IntegerField(required=True)
    student_id = serializers.IntegerField(required=True)

    def validate_submission_id(self, value):
        """
        Validate that the submission ID exists.
        """
        if not Essay.objects.filter(id=value).exists():
            raise serializers.ValidationError("The provided submission ID is invalid or does not exist.")
        return value

    def validate_student_id(self, value):
        """
        Validate that the student ID exists.
        """
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("The provided student ID is invalid or does not exist.")
        return value

class CreateAssignmentSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=True)
    class_id = serializers.IntegerField(required=True)
    due_date = serializers.DateField(required=True)
    expected_keywords = serializers.ListField(
        child=serializers.CharField(), min_length=25, max_length=30, required=True
    )

    def validate_due_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value


class UpdateAssignmentSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255)
    assignment_id = serializers.IntegerField(required=True)
    description = serializers.CharField(required=True)
    class_id = serializers.IntegerField(required=True)
    due_date = serializers.DateField(required=True)
    expected_keywords = serializers.ListField(
        child=serializers.CharField(), min_length=25, max_length=30, required=True
    )

    def validate_due_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value
