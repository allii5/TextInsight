from datetime import datetime
from django.utils import timezone


class UpdateAssignmentDTO:
    def __init__(self, data):
        self.title = data.get('title')
        self.assignment_id = data.get('assignment_id')
        self.description = data.get('description')
        self.class_id = data.get('class_id')
        self.due_date = data.get('due_date')
        self.expected_keywords = data.get('expected_keywords')
        self.errors = {}

        self._validate()

    def _validate(self):
        if not self.title:
            self.errors['title'] = 'Essay title is required.'
        if not self.assignment_id:
            self.errors['assignment_id'] = 'Assignment selection is required.'
        if not self.description:
            self.errors['description'] = 'Essay description is required.'
        if not self.class_id:
            self.errors['class_id'] = 'Class selection is required.'
        if not self.due_date:
            self.errors['due_date'] = 'Deadline is required.'
        else:
            parsed_due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            if parsed_due_date <= timezone.now().date():
                self.errors['due_date'] = 'Deadline must be in the future.'
        if not self.expected_keywords or not isinstance(self.expected_keywords, list):
            self.errors['expected_keywords'] = 'Expected keywords must be a list.'
        elif len(self.expected_keywords) < 25 or len(self.expected_keywords) > 30:
            self.errors['expected_keywords'] = 'Expected keywords must be between 25 and 30.'

    def is_valid(self):
        return len(self.errors) == 0

