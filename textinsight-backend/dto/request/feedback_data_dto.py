class FeedbackContentRequestDTO:
    def __init__(self, feedback_id):
        self.feedback_id = feedback_id
        self.errors = []
        self.validate()

    def validate(self):
        if self.feedback_id is None:
            self.errors.append("Feedback ID cannot be null.")
        elif not isinstance(self.feedback_id, int) or self.feedback_id <= 0:
            self.errors.append("Feedback ID must be a positive integer.")

    def is_valid(self):
        return not self.errors
