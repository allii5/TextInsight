import csv


class ClassDTO:
    def __init__(self, data, files):
        self.class_name = data.get('class_name')
        self.selected_usernames = data.getlist('selected_usernames', [])
        self.csv_file = files.get('csv_file')
        self.csv_usernames = []
        self.errors = {}

        self._validate()

    def _validate(self):
        if not self.class_name or len(self.class_name) > 100:
            self.errors['class_name'] = 'Class name must be provided and under 100 characters.'

        if self.csv_file:
            self._validate_csv_file()

    def _validate_csv_file(self):
        try:
            decoded_file = self.csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)

            next(csv_reader, None)

            self.csv_usernames = [
                row[0].strip() for row in csv_reader if row and row[0].strip()
            ]
            
        except Exception as e:
            self.errors['csv_file'] = 'Invalid CSV file format.'


    def is_valid(self):
        return len(self.errors) == 0
