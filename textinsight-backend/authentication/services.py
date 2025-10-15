from repositories.user_repository import UserRepository
from services.email_service import EmailService
from django.contrib.auth.hashers import make_password
from django.db import transaction
from datetime import datetime
import random
import string


class StudentAccountService:
    def __init__(self):
        self.user_repo = UserRepository()

    @transaction.atomic
    def handle_bulk_account_creation(self, valid_emails: list, number_of_accounts: int, teacher_email: str):
        """
        Handles bulk student account creation with validation, unique usernames, and email notifications.
        """
        try:
            # Fetch existing emails to avoid duplicates
            existing_emails = self.user_repo.get_existing_emails(valid_emails)
            unique_emails = list(set(valid_emails) - set(existing_emails))
            
            if len(unique_emails) == 0:
                EmailService.send_teacher_summary_email(
                    teacher_email,
                    created_accounts=[],
                    existing_emails=list(existing_emails),
                    unused_emails=[]
                )
                return {'status': 'error', 'message': 'No valid emails available for account creation.'}
            
            # Determine the number of accounts to create
            accounts_to_create = min(len(unique_emails), number_of_accounts)
            unused_emails = unique_emails[accounts_to_create:]
            accounts_created = []
            
            # Fetch last username to ensure uniqueness
            last_username_number = self.user_repo.get_last_username()
            
            for index, email in enumerate(unique_emails[:accounts_to_create]):
                username_number = last_username_number + index + 1
                username = f'SOTI{str(username_number).zfill(4)}'
                
                # Generate strong random password
                password = self._generate_strong_password()
                
                # Create user account
                user_data = {
                    'username': username,
                    'name': f"Student {username}",
                    'email': email,
                    'password': make_password(password),
                    'role': 'student',
                    'status': 'not_verified',
                    'class_count': 0,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                created_user = self.user_repo.create_user(user_data)
                
                if created_user:
                    accounts_created.append({
                        'username': username,
                        'email': email,
                    })
                    
                    # Send individual student account email
                    EmailService.send_student_account_email(
                        email=email,
                        username=username,
                        password=password
                    )
            
            # Send summary email to teacher
            EmailService.send_teacher_summary_email(
                teacher_email,
                created_accounts=accounts_created,
                existing_emails=list(existing_emails),
                unused_emails=unused_emails
            )
            
            # Send success email to teacher
            EmailService.send_teacher_success_email(
                teacher_email,
                total_accounts=len(accounts_created)
            )
            
            return {
                'status': 'success',
                'message': f'{len(accounts_created)} accounts have been successfully created.',
                'created_accounts': accounts_created,
                'existing_emails': list(existing_emails),
                'unused_emails': unused_emails
            }

        except Exception as e:
            print(f"Error during bulk account creation: {e}")
            return {'status': 'error', 'message': 'An error occurred during account creation.', 'details': str(e)}
    
    def _generate_strong_password(self, length: int = 8) -> str:
        """
        Generate a strong password containing uppercase, lowercase, digits, and special characters.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))
