from repositories.base_repository import BaseRepository
from typing import List, Dict
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from essay.models import Assignment

class AssignmentRepository(BaseRepository[Assignment]):
    """
    Initializes the AssignmentRepository class, inheriting from BaseRepository and setting the model to Assignment.
    This repository handles CRUD operations for the Assignment model.
    """
    def __init__(self):
        super().__init__(Assignment)

    """
    Finds assignments by class IDs.
    Returns a list of dictionaries containing assignment IDs and class IDs.
    Returns an empty list if an ObjectDoesNotExist or ValidationError occurs.
    """
    def findByClassId(self, class_ids: List[int]) -> List[Dict[str, str]]:
        try:
            assignments = self.model.objects.filter(class_id__in=class_ids)
            return [
                {
                    "assignment_id": assignment.id,
                    "class_id": assignment.class_id.id
                }
                for assignment in assignments
            ]
        except (ObjectDoesNotExist, ValidationError):
            return []
        
    """
    Retrieves the title of an assignment by its ID.
    Returns the title if the assignment is found, otherwise returns None.
    Returns None if an ObjectDoesNotExist, ValidationError, or any other exception occurs.
    """
    def titleById(self, assignmnet_id):

        try:

            assignment = self.model.objects.filter(
                id=assignmnet_id
            ).only('title').first()

            if assignment:
                return assignment.title 

           
            return None
        
        except (ObjectDoesNotExist, ValidationError, Exception):
            return None
    
    """
    Retrieves the expected keywords of an assignment by its ID.
    Returns the expected keywords if the assignment is found, otherwise returns an empty list.
    Returns an empty list if an ObjectDoesNotExist, ValidationError, or any other exception occurs.
    """
    def Expected_keywordsById(self, assignment_id):
        try:
           
            assignment = self.model.objects.filter(
                id=assignment_id
            ).only('expected_keywords').first()  

            if assignment:
                return assignment.expected_keywords  

            return []  

        except (ObjectDoesNotExist, ValidationError, Exception):
            return []

    """
    Retrieves the class ID of an assignment by its ID.
    Returns the class ID if the assignment is found, otherwise returns None.
    Returns None if an ObjectDoesNotExist, ValidationError, or any other exception occurs.
    """
    def classById(self, assignment_id):

        try:

            assignment_class_id = self.model.object.filter(
                id = assignment_id
            ).only('class_id')

            return assignment_class_id.value('class_id')
        
        except (ObjectDoesNotExist, ValidationError, Exception):
            return None

    def exists_by_id_and_class(self, assignment_id: int, class_id: int) -> bool:
        """
        Check if an assignment exists with the given assignment ID and class ID.
        
        Args:
            assignment_id (int): The ID of the assignment.
            class_id (int): The ID of the class.

        Returns:
            bool: True if the assignment exists, False otherwise.
        """
        try:
            return self.model.objects.filter(id=assignment_id, class_id=class_id).exists()
        except Exception as e:
            print(f"Error checking assignment existence: {e}")
            return False
        
    def get_assignments_by_class_ids(self, class_ids):
        if not isinstance(class_ids, (list, tuple, set)):
            raise ValueError("class_ids must be a list, tuple, or set of IDs.")
        
        return self.model.objects.filter(class_id__in=class_ids).order_by('-created_at')
    
    def get_assignments_by_class_ids_dashbaord(self, class_ids):
        if not isinstance(class_ids, (list, tuple, set)):
            raise ValueError("class_ids must be a list, tuple, or set of IDs.")
        
        return self.model.objects.filter(class_id__in=class_ids).order_by('-created_at')[:2]
    
    def get_assignment_by_id(self, assignment_id):
        return self.model.objects.filter(id=assignment_id).first()