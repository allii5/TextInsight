class ProgressContentRequestDTO:
    def __init__(self, progress_id):
        self.progress_id = progress_id
        self.errors = []
        self.validate()

    def validate(self):
        if self.progress_id is None:
            self.errors.append("Progress ID cannot be null.")
        elif not isinstance(self.progress_id, int) or self.progress_id <= 0:
            self.errors.append("Progress ID must be a positive integer.")

    def is_valid(self):
        return not self.errors
