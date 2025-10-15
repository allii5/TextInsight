from repositories.base_repository import BaseRepository
from typing import List, Dict
from django.core.exceptions import ValidationError
from essay.models import Essay, Assignment
from repositories.assignment_repository import AssignmentRepository
from repositories.class_repository import ClassStudentsRepository
from repositories.feedback_repository import FeedbackRepository
from datetime import datetime
from custom_error_classes import AssignmentNotFoundError, DueDatePassedError, FeedbackNotAvailableError, UserNotInClassError, SubmissionLimitExceededError
import logging

logging.basicConfig(level=logging.ERROR)

class EssayRepository(BaseRepository[Essay]):
    """
    Initializes the EssayRepository class, inheriting from BaseRepository and setting the model to Essay.
    Initializes the AssignmentRepository, ClassStudentsRepository, and FeedbackRepository for handling related operations.
    """
    def __init__(self):
        super().__init__(Essay)
        self.assignment_repo = AssignmentRepository()
        self.class_students_repo = ClassStudentsRepository()
        self.feedback_repo = FeedbackRepository()

    """
    Finds essays by student ID and assignment IDs.
    Returns a list of dictionaries containing assignment details for assignments that have less than two submissions.
    Returns an empty list if a ValidationError occurs or if an error occurs.
    """
    def findByStudentIdAndAssignmentId(self, student_id: int, assignment_ids: List[int]) -> List[Dict]:
        try:
            submissions_with_two_submissions = self.model.objects.filter(
                student_id=student_id,
                assignment_id__in=assignment_ids,
                submission_count=2
            ).values_list('assignment_id', flat=True)

            unmatched_assignment_ids = set(assignment_ids) - set(submissions_with_two_submissions)

            unmatched_assignments = Assignment.objects.filter(
                id__in=list(unmatched_assignment_ids),
                due_date__gt=datetime.now()  
            ).select_related('class_id')

            result = []

            for assignment in unmatched_assignments:
                
                single_submission = self.model.objects.filter(
                    student_id=student_id,
                    assignment_id=assignment.id,
                    submission_count=1
                ).first()

               
                submission_count = 1 if single_submission else 0
                last_submission = single_submission.submission_date.strftime("%d %b %y") if single_submission else ""

                result.append({
                    "assignment_id": assignment.id,
                    "assignment_name": assignment.title,
                    "class_id": assignment.class_id.id,
                    "class_name": assignment.class_id.class_name,
                    "class_code": assignment.class_id.class_code,
                    "teacher_name": assignment.class_id.teacher_name,
                    "last_submission" :last_submission,
                    "due_date": assignment.due_date.strftime("%d %b %y"),  
                    "submission_count": submission_count
                })

            return result

        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    """
    Saves a new essay submission.
    Validates the assignment, checks the due date, ensures the user is part of the class, and handles submission count logic.
    Returns the saved essay if successful, otherwise returns None.
    """  
    def save_submission(self, assignment_id, user, essay_text):
        try:
            assignment = self.assignment_repo.findById(assignment_id)

            if assignment is None or assignment.class_id is None:
                raise AssignmentNotFoundError("Assignment not found or does not belong to a class.")
            
            if assignment.due_date and assignment.due_date < datetime.now().date():
                raise DueDatePassedError("The assignment's due date has passed; submissions are no longer allowed.")
            
            if not self.class_students_repo.findByClassId(user.id, assignment.class_id):
                raise UserNotInClassError("User is not part of the class.")
            
            check_prev = self.checkPreviousSubmission(user.id, assignment_id)

            if check_prev is None:
                submission_count = 1
            elif check_prev["submission_count"] == 1:
                if not self.feedback_repo.check_user_have_inter_essay_feedback(user.id, check_prev["id"], assignment_id): 
                    raise FeedbackNotAvailableError("Inter-essay feedback not generated; cannot submit again.")
                
                self.updateById(check_prev["id"], {"status": "resubmitted"})
                submission_count = 2
            elif check_prev["submission_count"] >= 2:
                raise SubmissionLimitExceededError("You cannot submit the essay more than two times.")
            
            essay = self.create({
                "title": assignment.title,
                "content": essay_text,
                "student": user,
                "assignment": assignment,
                "submission_count": submission_count
            })

            return essay

        except (AssignmentNotFoundError, DueDatePassedError, UserNotInClassError, 
                FeedbackNotAvailableError, SubmissionLimitExceededError) as e:
            logging.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            raise

    """
    Checks for previous submissions by a user for a specific assignment.
    Returns a dictionary containing the submission ID and count if found, otherwise returns None.
    """
    def checkPreviousSubmission(self, user_id, assignment_id):
        try:
            submissions = self.model.objects.filter(
                student=user_id,
                assignment_id=assignment_id
            ).only('id', 'submission_count').order_by('submission_count')  

            if not submissions.exists():
                return None  

            submission_with_count_2 = submissions.filter(submission_count=2).first()
            if submission_with_count_2:
                return {
                    "id": submission_with_count_2.id,
                    "submission_count": submission_with_count_2.submission_count
                }

            submission_with_count_1 = submissions.filter(submission_count=1).first()
            if submission_with_count_1:
                return {
                    "id": submission_with_count_1.id,
                    "submission_count": submission_with_count_1.submission_count
                }

            return None  

        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    """
    Retrieves the submission history for a user.
    Returns a list of dictionaries containing submission details, ordered by submission date.
    Returns an empty list if a ValidationError occurs or if an error occurs.
    """
    def submissionHistory(self, user_id):

        try:

            submissions = self.model.objects.filter(
                student_id = user_id
            ).order_by('-submission_date').values_list('id', 'title', 'assignment_id', 'submission_date')

            result = []

            for id, title, assignment_id, submission_date in submissions:

                assignment = self.assignment_repo.findById(assignment_id)

                result.append({
                    'id': id,
                    'title' : title,
                    'class_code' : assignment.class_id.class_code,
                    'assignment_id' : assignment_id,
                    "submitted": submission_date.strftime("%d %b %y"),
                })
            

            return result
        
        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    """
    Retrieves the specific submission content by submission ID.
    Returns a dictionary containing the submission ID, title, and content if found, otherwise returns None.
    """
    def specficSubmissionContent(self, submission_id):
        try:
            content = self.model.objects.filter(id=submission_id).values_list('id', 'title', 'content').first()

            if content:
                return {
                    'id': content[0],
                    'title': content[1],
                    'content': content[2]
                }
            else:
                return None

        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    """
    Retrieves the specific submission content for a user by submission ID.
    Returns a dictionary containing the submission ID, title, and content if found, otherwise returns None.
    """
    def specificSubmissionContentOfUser(self, user, submission_id):
        try:
            content = self.model.objects.filter(student = user,id=submission_id).values_list('id', 'title', 'content').first()

            if content:
                return {
                    'id': content[0],
                    'title': content[1],
                    'content': content[2]
                }
            else:
                print(f"Validation error (Student does not have submission with this id)")
                return None

        except ValidationError as e:
            print(f"Validation error (Student does not have submission with this id): {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    """
    Retrieves the submission history for the dashboard for a user.
    Returns a list of dictionaries containing the most recent submission details, limited to the last two submissions.
    Returns an empty list if a ValidationError occurs or if an error occurs.
    """
    def submissionHistoryDashboard(self, user_id):

        try:

            submissions = self.model.objects.filter(
                student_id = user_id
            ).order_by('-submission_date').values_list('id', 'title', 'assignment_id', 'submission_date')[:2]

            result = []

            for id, title, assignment_id, submission_date in submissions:

                assignment = self.assignment_repo.findById(assignment_id)

                result.append({
                    'id': id,
                    'title' : title,
                    'class_code' : assignment.class_id.class_code,
                    "teacher_name": assignment.class_id.teacher_name,
                    'assignment_id' : assignment_id,
                    "submitted": submission_date.strftime("%d %b %y"),
                })
            

            return result
        
        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
    """
    Finds essays by student ID and assignment IDs for the dashboard.
    Returns a list of dictionaries containing assignment details for assignments that have less than two submissions.
    Returns an empty list if a ValidationError occurs or if an error occurs.
    """
    def findByStudentIdAndAssignmentIdDashboard(self, student_id: int, assignment_ids: List[int]) -> List[Dict]:
        try:
            submissions_with_two_submissions = self.model.objects.filter(
                student_id=student_id,
                assignment_id__in=assignment_ids,
                submission_count=2
            ).values_list('assignment_id', flat=True)

            unmatched_assignment_ids = set(assignment_ids) - set(submissions_with_two_submissions)

            unmatched_assignments = Assignment.objects.filter(
                id__in=list(unmatched_assignment_ids),
                due_date__gt=datetime.now()  
            ).select_related('class_id')[:2]

            result = []

            for assignment in unmatched_assignments:
                
                single_submission = self.model.objects.filter(
                    student_id=student_id,
                    assignment_id=assignment.id,
                    submission_count=1
                ).exists()

               
                submission_count = 1 if single_submission else 0

                result.append({
                    "assignment_id": assignment.id,
                    "assignment_name": assignment.title,
                    "class_code": assignment.class_id.class_code,
                    "teacher_name": assignment.class_id.teacher_name,
                    "due_date": assignment.due_date.strftime("%d %b %y"),  
                    "submission_count": submission_count
                })

            return result

        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []


    def get_students_who_submitted_essays(self, assignment_id):
            """
            Fetches the student IDs who have submitted essays for the given assignment.
            Parameters:
                assignment_id: ID of the assignment.
            Returns:
                QuerySet of essays with related student details.
            """
            return self.model.objects.filter(assignment_id=assignment_id).select_related('student')