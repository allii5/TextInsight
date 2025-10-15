from django.db.models import Q
from repositories.base_repository import BaseRepository
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from authentication.models import User, Notification
from repositories.notification_repository import NotificationRepository
from django.db import models

class UserRepository(BaseRepository[User]):
    """
    Initializes the UserRepository class, inheriting from BaseRepository and setting the model to User.
    Initializes the NotificationRepository for handling notification-related operations.
    """
    def __init__(self):
        super().__init__(User)
        self.notification_repo = NotificationRepository()

    """
    Updates a user record by ID with the provided update data.
    If the update data contains a list of notification IDs, it adds these notifications to the user's notifications.
    Otherwise, it updates the specified fields of the user record.
    Returns True if the update is successful, False otherwise.
    """
    def updateById(self, model_id: int, update_data: dict) -> bool:
        try:
            document = self.model.objects.get(id=model_id)
            
            for field, value in update_data.items():
                if field == "notifications" and isinstance(value, list):
                    notifications_to_add = Notification.objects.filter(id__in=value)
                    document.notifications.add(*notifications_to_add)
                else:
                    setattr(document, field, value)
            
            document.save()
            return True
        
        except (ObjectDoesNotExist, ValidationError):
            return False
    
    """
    Fetches unread notifications for a user by user ID.
    Marks the notifications as read and returns a list of notification messages.
    Returns an empty list if the user is not found or if an error occurs.
    """
    def fetch_unread_notifications(self, user_id):
        try:
            user = self.model.objects.get(id=user_id)
            
            unread_notifications = user.notifications.filter(status="unread").order_by('-created_at').only('id', 'message')
            
            notification_messages = [notification.message for notification in unread_notifications]

            for notification in unread_notifications:
                success = self.notification_repo.updateById(notification.id, {"status": "read"})
                if not success:
                    print(f"Failed to update notification with ID: {notification.id}")
            
            return notification_messages

        except User.DoesNotExist:
            print("User not found.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_existing_emails(self, emails):
        """Fetch existing emails from the database."""
        return set(self.model.objects.filter(email__in=emails).values_list('email', flat=True))

    def get_last_username(self):
        """Fetch the last created username starting with 'SOTI'."""
        last_user = self.model.objects.filter(username__startswith='SOTI').order_by('-username').first()
        if last_user and last_user.username[4:].isdigit():
            return int(last_user.username[4:])
        return 0

    def create_user(self, data):
        """Create a user instance in the database."""
        return self.create(data)
    
    def get_existing_usernames(self, usernames):
        return list(User.objects.filter(username__in=usernames).values_list('username', flat=True))

    def get_by_id(self, user_id):
        return User.objects.filter(id=user_id).first()

    def increment_class_count(self, user_id):
        User.objects.filter(id=user_id).update(class_count=models.F('class_count') + 1)

    def increment_class_count_for_students(self, usernames):
        User.objects.filter(username__in=usernames).update(class_count=models.F('class_count') + 1)
    
    def get_by_username(self, username):
        try:
            return self.model.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"No user found with username: {username}")
    
    def find_by_ids(self, user_ids):
        """
        Fetches user objects by a list of IDs.
        Parameters:
            user_ids: List of user IDs.
        Returns:
            QuerySet of user objects.
        """
        return self.model.objects.filter(id__in=user_ids)
    
    def search_students(self, search_query=None):
        """
        Fetches all students in the database, excluding teachers.
        Optionally filters by username or name.
        """
        # Filter users by role (exclude teachers)
        students_query = User.objects.filter(role='student').exclude(role='teacher')

        # If a search query is provided, apply filtering by username or name
        if search_query:
            students_query = students_query.filter(
                Q(username__icontains=search_query) | Q(name__icontains=search_query)
            )

        return [
            {
                "id": student.id,
                "username": student.username,
                "name": student.name,
                "email": student.email,
            }
            for student in students_query
        ]
