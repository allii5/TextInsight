from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class EmailService:
    @staticmethod
    def send_student_account_email(email, username, password):
        """Send account creation details to a student."""
        subject = "Your Student Account has been Created"
        context = {
            'username': username,
            'password': password,
            'frontend_url': settings.FRONTEND_URL,
        }
        html_message = render_to_string('emails/student_account_created.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)

    @staticmethod
    def send_teacher_summary_email(teacher_email, created_accounts, existing_emails, unused_emails):
        """Send summary email to the teacher."""
        subject = "Student Account Creation Summary"
        context = {
            'created_accounts': created_accounts,
            'existing_emails': existing_emails,
            'unused_emails': unused_emails,
        }
        html_message = render_to_string('emails/teacher_summary.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [teacher_email], html_message=html_message)

    @staticmethod
    def send_teacher_success_email(teacher_email, total_accounts):
        """Send a success email to the teacher after account creation."""
        subject = "Student Accounts Successfully Created"
        context = {
            'total_accounts': total_accounts,
        }
        html_message = render_to_string('emails/teacher_success.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [teacher_email], html_message=html_message)

    @staticmethod
    def notify_student_added_to_class(student_email, student_name, class_name, teacher_name):
        subject = "You’ve Been Added to a New Class"
        context = {
            'student_name': student_name,
            'class_name': class_name,
            'teacher_name': teacher_name,
            'frontend_url': settings.FRONTEND_URL,
        }
        html_message = render_to_string('emails/student_added_to_class.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [student_email], html_message=html_message)

    @staticmethod
    def notify_teacher_class_created(teacher_email, teacher_name, class_name, class_code, student_count):
        subject = "Your Class Has Been Created"
        context = {
            'teacher_name': teacher_name,
            'class_name': class_name,
            'class_code': class_code,
            'student_count': student_count,
        }
        html_message = render_to_string('emails/class_created.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [teacher_email], html_message=html_message)