class SubmissionContentRequestDTO:
    def __init__(self, submission_id):
        self.submission_id = submission_id
        self.errors = []
        self.validate()

    def validate(self):
        if self.submission_id is None:
            self.errors.append("Submission ID cannot be null.")
        elif not isinstance(self.submission_id, int) or self.submission_id <= 0:
            self.errors.append("Submission ID must be a positive integer.")

    def is_valid(self):
        return not self.errors
