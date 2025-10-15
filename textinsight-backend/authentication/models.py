from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Notification(models.Model):
    message = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[("read", "Read"), ("unread", "Unread")], default="unread")
    created_at = models.DateTimeField(default=timezone.now)

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=[("student", "Student"), ("teacher", "Teacher")], default="student")
    status = models.CharField(max_length=20, choices=[("verified", "Verified"), ("not_verified", "Not Verified")], default="not_verified")
    education_level = models.CharField(max_length=255, blank=True, null=True)
    class_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    notifications = models.ManyToManyField(Notification)
    first_time_login = models.BooleanField(default=True)  # Add this flag


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def send_verification_email(user, action):
        """
        Sends a verification email to the user with a personalized link and action.
        Parameters:
            user: The user object to whom the email is sent.
            action: The purpose of the verification (e.g., 'create_account', 'reset_password').
        """
        # Validate the action
        valid_actions = ["create_account", "reset_password"]
        if action not in valid_actions:
            raise ValueError(f"Invalid action. Supported actions are: {valid_actions}")

        # Generate uid and token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construct verification link with action
        verification_link = f"{settings.FRONTEND_URL}/emailverification?uid={uid}&token={token}&action={action}"
        
        # Email content
        subject = "Verify Your Account - TextInsight"
        if action == "reset_password":
            subject = "Reset Your Password - TextInsight"

        context = {
            'username': user.username,
            'verification_link': verification_link,
            'action': action,
        }
        html_message = render_to_string('emails/verify_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
        )


    # def send_verification_email(self):
    #     token_generator = PasswordResetTokenGenerator()
    #     token = token_generator.make_token(self)
    #     uid = urlsafe_base64_encode(force_bytes(self.pk))
    #     verification_link = f"{settings.FRONTEND_URL}/verify-email?uid={uid}&token={token}"
        
    #     send_mail(
    #         subject="Verify Your Email",
    #         message=f"Please verify your email by clicking the following link: {verification_link}",
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[self.email],
    #     )

    def send_welcome_email(self, plain_password):
        """Send a welcome email with the student's username and plain password."""
        username = self.username
        email_subject = "Welcome to the platform"
        email_message = f"Hello {username},\n\nYour account has been created successfully.\n\n" \
                        f"Username: {username}\nPassword: {plain_password}\n\n" \
                        "Please change your password after logging in for the first time."

        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email],
        )

    def generate_unique_username(self, email):
        # Extract the part before "@" from the email
        base_username = email.split('@')[0]

        # Check if the username already exists
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        return username