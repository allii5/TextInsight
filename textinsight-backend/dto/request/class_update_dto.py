class UpdateClassDTO:
    def __init__(self, data):
        self.class_name = data.get('class_name')
        self.class_id = data.get('class_id')
        self.added_usernames = data.getlist('added_usernames', [])
        self.errors = {}

        print(self.added_usernames)
        self._validate()

    def _validate(self):
        if self.class_name and len(self.class_name) > 100:
            self.errors['class_name'] = "Class name must be under 100 characters."
        if not self.class_name:
            self.errors['class_name'] = "Class name must be provided."
        if not self.class_id:
            self.errors['class_id'] = "Class id must be provided."

    def is_valid(self):
        return len(self.errors) == 0
