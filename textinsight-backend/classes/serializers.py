from rest_framework import serializers
import csv

class UpdateClassSerializer(serializers.Serializer):
    class_name = serializers.CharField(max_length=100, required=True)
    class_id = serializers.IntegerField(required=True)
    added_usernames = serializers.ListField(
        child=serializers.CharField(), required=False, default=[]
    )

    def validate_class_name(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Class name must be under 100 characters.")
        return value

class CreateClassSerializer(serializers.Serializer):
    class_name = serializers.CharField(max_length=100, required=True)
    selected_usernames = serializers.ListField(
        child=serializers.CharField(), required=False, default=[]
    )
    csv_file = serializers.FileField(required=False)

    csv_usernames = []

    def validate_class_name(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Class name must be under 100 characters.")
        return value

    def validate_csv_file(self, value):
        try:
            decoded_file = value.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)

            # Skip the header row (if present)
            next(csv_reader, None)

            # Extract usernames from the CSV
            self.csv_usernames = [
                row[0].strip() for row in csv_reader if row and row[0].strip()
            ]

            if not self.csv_usernames:
                raise serializers.ValidationError("CSV file contains no valid usernames.")

        except Exception:
            raise serializers.ValidationError("Invalid CSV file format.")

        return value