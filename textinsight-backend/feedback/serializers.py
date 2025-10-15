from rest_framework import serializers

class FeedbackContentRequestSerializer(serializers.Serializer):
    feedback_id = serializers.IntegerField()

    def validate_feedback_id(self, value):
        """
        Custom validation for the feedback_id field.
        Ensures it is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Feedback ID must be a positive integer.")
        return value


class ProgressContentRequestSerializer(serializers.Serializer):
    progress_id = serializers.IntegerField()

    def validate_progress_id(self, value):
        """
        Custom validation for the progress_id field.
        Ensures it is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Progress ID must be a positive integer.")
        return value

class AssignmentQuerySerializer(serializers.Serializer):
    """
    Serializer for validating query parameters, specifically `assignment_id`.
    """
    assignment_id = serializers.IntegerField(required=True, error_messages={
        "required": "The 'assignment_id' query parameter is required.",
        "invalid": "The 'assignment_id' must be a valid integer."
    })

class FeedbackQuerySerializer(serializers.Serializer):
    """
    Serializer for validating feedback_id and student_id query parameters.
    """
    feedback_id = serializers.IntegerField(required=True, error_messages={
        "required": "The 'feedback_id' query parameter is required.",
        "invalid": "The 'feedback_id' must be a valid integer."
    })
    student_id = serializers.IntegerField(required=True, error_messages={
        "required": "The 'student_id' query parameter is required.",
        "invalid": "The 'student_id' must be a valid integer."
    })

class ProgressQuerySerializer(serializers.Serializer):
    """
    Serializer for validating progress_id and student_id query parameters.
    """
    progress_id = serializers.IntegerField(required=True, error_messages={
        "required": "The 'progress_id' query parameter is required.",
        "invalid": "The 'progress_id' must be a valid integer."
    })
    student_id = serializers.IntegerField(required=True, error_messages={
        "required": "The 'student_id' query parameter is required.",
        "invalid": "The 'student_id' must be a valid integer."
    })