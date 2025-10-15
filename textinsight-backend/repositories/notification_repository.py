from repositories.base_repository import BaseRepository
from authentication.models import Notification

class NotificationRepository(BaseRepository[Notification]):
    """
    Initializes the NotificationRepository class, inheriting from BaseRepository and setting the model to Notification.
    This repository handles CRUD operations for the Notification model.
    """
    def __init__(self):
        super().__init__(Notification)

    

    

    