from django.db.models import Q
from repositories.base_repository import BaseRepository
from typing import List, Dict
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from classes.models import Class, ClassStudents
from authentication.models import User
from repositories.user_repository import UserRepository

class ClassRepository(BaseRepository[Class]):
    """
    Initializes the ClassRepository class, inheriting from BaseRepository and setting the model to Class.
    This repository handles CRUD operations for the Class model.
    """
    def __init__(self):
        super().__init__(Class)

    """
    Finds classes by their IDs and returns a list of dictionaries containing class details.
    Returns an empty list if a ValidationError occurs.
    """
    def findByClassIds(self, class_ids: List[int]) -> List[Dict[str, str]]:
        try:
            classes = self.model.objects.filter(id__in=class_ids)
            return [
                {
                    "class_name": class_obj.class_name,
                    "class_code": class_obj.class_code,
                    "teacher_name": class_obj.teacher_name
                }
                for class_obj in classes
            ]
        except ValidationError:
            return []
    
    def get_classes_by_teacher(self, teacher_id):
        """Fetch classes created by the given teacher."""
        return self.model.objects.filter(teacher_id=teacher_id)

    def get_last_class_code(self):
        """
        Retrieve the last class code from the database.
        Returns the last class code if it exists, or None if no classes are present.
        """
        last_class = (
            self.model.objects.order_by('-created_at').first()  # Adjust based on your model fields
        )
        return last_class.class_code if last_class else None
    
    def get_teacher_classes(self, teacher_id):
        return self.model.objects.filter(teacher_id=teacher_id)
    
    def get_teacher_classes_dashboard(self, teacher_id):
        return self.model.objects.filter(teacher_id=teacher_id)[:2]


class ClassStudentsRepository(BaseRepository[ClassStudents]):
    """
    Initializes the ClassStudentsRepository class, inheriting from BaseRepository and setting the model to ClassStudents.
    This repository handles CRUD operations for the ClassStudents model.
    """
    def __init__(self):
        super().__init__(ClassStudents)
        self.user_repo = UserRepository()

    """
    Finds class IDs associated with a student by their student ID.
    Returns a list of class IDs or an empty list if an ObjectDoesNotExist or ValidationError occurs.
    """
    def findByStudentId(self, student_id: int) -> List[int]:
        try:
            class_students = self.model.objects.filter(student_id=student_id)
            return [class_student.class_id.id for class_student in class_students]
        except (ObjectDoesNotExist, ValidationError):
            return []
        
    """
    Checks if a student is enrolled in a specific class by their student ID and class ID.
    Returns True if the student is enrolled, False if an ObjectDoesNotExist or ValidationError occurs.
    """
    def findByClassId(self, student_id: int, class_id: int):
        try:
            return self.model.objects.filter(
                student_id=student_id,
                class_id=class_id
            ).exists()
        except (ObjectDoesNotExist, ValidationError):
            return False

    def add_students_to_class(self, class_id, usernames):
        students = []
        student_objects = User.objects.filter(username__in=usernames)

        for student in student_objects:
            students.append(
                self.model(
                    class_id_id=class_id,
                    student_id=student
                )
            )
        self.model.objects.bulk_create(students)
    
    def is_student_in_class(self, class_id, student_username):
        """
        Check if a student is already enrolled in the class.

        Args:
            class_id (int): The class ID.
            student_id (int): The student ID.

        Returns:
            bool: True if the student is enrolled, False otherwise.
        """

        student = self.user_repo.get_by_username(student_username)
        return ClassStudents.objects.filter(class_id=class_id, student_id=student.id).exists()
    
    def get_students_in_class(self, class_id, search_query=None):
        """
        Fetches students in a specific class. If a search query is provided, it filters by username or name.

        Args:
            class_id (int): The class ID.
            search_query (str, optional): A query to filter students by username or name.

        Returns:
            List[Dict[str, str]]: A list of students with their details.
        """
        students_query = User.objects.filter(
            student_classes__class_id=class_id  # Correct relationship name here
        ).exclude(role='teacher')

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

