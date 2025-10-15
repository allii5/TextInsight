from repositories.base_repository import BaseRepository
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from feedback.models import Progress
from repositories.assignment_repository import AssignmentRepository

class ProgressRepository(BaseRepository[Progress]):
    """
    Initializes the ProgressRepository class, inheriting from BaseRepository and setting the model to Progress.
    Initializes the AssignmentRepository for handling related operations.
    """
    def __init__(self):
        super().__init__(Progress)
        self.assignment_repo = AssignmentRepository()

    """
    Retrieves the progress history for a user.
    Returns a list of dictionaries containing the progress details if found, otherwise returns an empty list.
    """
    def progressHistory(self, user_id):

        try:

            progress_s = self.model.objects.filter(
                student_id = user_id
            ).order_by('-progress_date').values_list('id', 'assignment_id', 'progress_date')

            result = []

            for id, assignment_id, progress_date in progress_s:

                assignment = self.assignment_repo.findById(assignment_id)

                result.append({
                    'id': id,
                    'title' : assignment.title,
                    'class_code' : assignment.class_id.class_code,
                    'assignment_id' : assignment_id,
                    "feedback_on": progress_date.strftime("%d %b %y"),
                })
            

            return result
        
        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        
    """
    Retrieves the specific progress data by feedback ID.
    Returns a dictionary representation of the progress data if found, otherwise returns None.
    """
    def specficProgressdata(self, feedback_id):
        try:
            data = self.model.objects.get(id=feedback_id) 
            return model_to_dict(data)  

        except self.model.DoesNotExist:
            print("No matching data found.")
            return None
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    """
    Retrieves the specific progress data for a user by feedback ID.
    Returns a dictionary representation of the progress data if found, otherwise returns None.
    """
    def specficProgressDataOfUser(self,user_id, feedback_id):
        try:
            data = self.model.objects.get(student_id = user_id,id=feedback_id) 
            return model_to_dict(data)  

        except self.model.DoesNotExist:
            print("No matching data found.")
            return None
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    """
    Retrieves the progress history for the dashboard for a user.
    Returns a list of dictionaries containing the most recent progress details, limited to the last two submissions.
    Returns an empty list if a ValidationError occurs or if an error occurs.
    """
    def progressHistoryDashboard(self, user_id):

        try:

            progress_s = self.model.objects.filter(
                student_id = user_id
            ).order_by('-progress_date').values_list('id', 'assignment_id', 'progress_date')[:2]

            result = []

            for id, assignment_id, progress_date in progress_s:

                assignment = self.assignment_repo.findById(assignment_id)

                result.append({
                    'id': id,
                    'title' : assignment.title,
                    'class_code' : assignment.class_id.class_code,
                    "teacher_name": assignment.class_id.teacher_name,
                    'assignment_id' : assignment_id,
                    "feedback_on": progress_date.strftime("%d %b %y"),
                })
            

            return result
        
        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    

    def get_students_with_progress(self, assignment_id):
        """
        Fetches the IDs of students who have received progress for a given assignment.
        Parameters:
            assignment_id: ID of the assignment.
        Returns:
            QuerySet of student IDs and their progress IDs.
        """
        return self.model.objects.filter(assignment_id=assignment_id).values_list('student_id', 'id', 'progress_date')
    