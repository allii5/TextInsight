class EssaySubmissionDTO:
    def __init__(self, data):
        self.assignment_id = data.get('assignment_id')
        self.introduction = data.get('introduction')
        self.middle = data.get('middle')
        self.conclusion = data.get('conclusion')
        self.errors = {}

        self._validate()

    def _validate(self):
        if not self.assignment_id:
            self.errors['assignment_id'] = 'This field is required.'
        if not self.introduction:
            self.errors['introduction'] = 'This field is required.'
        if not self.middle:
            self.errors['middle'] = 'This field is required.'
        if not self.conclusion:
            self.errors['conclusion'] = 'This field is required.'

    def is_valid(self):
        return len(self.errors) == 0
