from django.utils.crypto import get_random_string
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import csv
import re
# import dns.resolver

class SignupTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password', 'education_level']
    
    def create(self, validated_data):
        validated_data['role'] = 'teacher'
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# class ResetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

#     def save(self):
#         email = self.validated_data['email']
#         password = make_password(self.validated_data['password'])
#         user = User.objects.get(email=email)
#         user.password = password
#         user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Ensure the email exists in the database
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def save(self):
        uid = self.validated_data['uid']
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']

        # Decode UID and get user
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid user ID."})

        # Validate the token
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        # Update the password
        user.set_password(new_password)
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def validate_current_password(self, value):
        if not self.user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()


class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']  # Only email and password fields

    def create(self, validated_data):
        email = validated_data.get('email')
        
        # Generate a username from the email
        username = self.generate_username_from_email(email)

        # If no password is provided, generate a random password
        password = self.generate_random_password()
        plain_password = password  # Save the plain password to send in the welcome email

        # Hash the password before saving
        password = make_password(password)
        
        # Create the student user
        user = User.objects.create(username=username, email=email, password=password, role="student")
        
        # Send welcome email with the plain password
        user.send_welcome_email(plain_password)
        # Return the created user instance
        return user

    def generate_username_from_email(self, email):
        """Generate a username from the email."""
        username = email.split('@')[0]  # Extract the part before '@'

        # Ensure the username is unique
        if User.objects.filter(username=username).exists():
            postfix = 1
            while User.objects.filter(username=f"{username}_{postfix}").exists():
                postfix += 1
            username = f"{username}_{postfix}"

        return username

    def generate_random_password(self, length=8):
        """Generate a random password."""
        return get_random_string(length=length, allowed_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")



class FirstTimeLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        user = User.objects.get(username=username, role='student', first_time_login=True)
        user.email = email
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['role'] = self.user.role
        data['email'] = self.user.email
        data['first_time_login'] = self.user.first_time_login
        data['status'] = self.user.status
        
        return data

class StudentAccountsSerializer(serializers.Serializer):
    number_of_accounts = serializers.IntegerField()
    csv_file = serializers.FileField()

    valid_emails = serializers.ListField(child=serializers.EmailField(), read_only=True)
    invalid_emails = serializers.ListField(child=serializers.EmailField(), read_only=True)
    duplicate_emails = serializers.ListField(child=serializers.EmailField(), read_only=True)
    errors = serializers.DictField(child=serializers.CharField(), read_only=True)

    def validate_number_of_accounts(self, value):
        """Validate the number of accounts."""
        if value < 1 or value > 50:
            raise serializers.ValidationError("Number of accounts must be between 1 and 50.")
        return value

    def validate_csv_file(self, value):
        """Validate the uploaded CSV file."""
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        # Read and validate the file contents
        try:
            decoded_file = value.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            headers = next(csv_reader, None)

            if not headers or 'email' not in headers[0].lower():
                raise serializers.ValidationError('CSV file must have an "email" column.')
            
            
            valid_email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
            seen_emails = set()
            valid_emails = []
            invalid_emails = []
            duplicate_emails = []

            for row in csv_reader:
                if row:
                    email = row[0].strip()
                    if email in seen_emails:
                        duplicate_emails.append(email)
                    else:
                        seen_emails.add(email)
                        if not valid_email_pattern.match(email):
                            invalid_emails.append(email)
                        else:
                            valid_emails.append(email)

            # Add the result to the validated data
            self.valid_emails = valid_emails
            self.invalid_emails = invalid_emails
            self.duplicate_emails = duplicate_emails

            if len(valid_emails) == 0:
                raise serializers.ValidationError('No valid emails found in the uploaded CSV file. Please check and re-upload.')

        except UnicodeDecodeError:
            raise serializers.ValidationError('Unable to read the file. Please upload a valid CSV file.')
        except Exception as e:
            raise serializers.ValidationError(f'An error occurred while validating the file: {e}')
        
        return value


    def to_representation(self, instance):
        """Modify the output structure."""
        return {
            'valid_emails': self.valid_emails,
            'invalid_emails': self.invalid_emails,
            'duplicate_emails': self.duplicate_emails,
            'requested_accounts': self.validated_data.get('number_of_accounts'),
            'valid_email_count': len(self.valid_emails),
            'errors': self.errors
        }