from typing import TypeVar, Generic, List, Optional
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

T = TypeVar('T', bound=models.Model)

class BaseRepository(Generic[T]):
    """
    Initializes the BaseRepository class with a specified model.
    This base repository provides generic CRUD operations for any Django model.
    """
    def __init__(self, model: T):
        self.model = model

    """
    Finds a record by its ID.
    Returns the record if found, otherwise returns None.
    """
    def findById(self, model_id: int) -> Optional[T]:
        try:
            return self.model.objects.get(id=model_id)
        except (ObjectDoesNotExist, ValidationError):
            return None

    """
    Retrieves all records from the database.
    Returns a list of all records.
    """
    def findAll(self) -> List[T]:
        return self.model.objects.all()

    """
    Updates a record by its ID with the provided update data.
    Returns True if the update is successful, False otherwise.
    """
    def updateById(self, model_id, update_data: dict) -> bool:
        try:
            document = self.model.objects.get(id=model_id)
            for field, value in update_data.items():
                setattr(document, field, value)
            document.save()
            return True
        except (ObjectDoesNotExist, ValidationError):
            return False

    """
    Deletes a record by its ID.
    Returns True if the deletion is successful, False otherwise.
    """
    def deleteById(self, model_id: int) -> bool:
        try:
            document = self.model.objects.get(id=model_id)
            document.delete()
            return True
        except (ObjectDoesNotExist, ValidationError):
            return False

    """
    Creates a new record with the provided data.
    Returns the newly created record if successful, None otherwise.
    """
    def create(self, data: dict) -> Optional[T]:
        try:
            new_document = self.model(**data)
            new_document.save()
            return new_document
        except ValidationError as e:
            print(f"Error creating document: {e}")
            return None

    """
    Counts the number of records in the database.
    Returns the total count of records.
    """
    def count(self) -> int:
        return self.model.objects.count()
