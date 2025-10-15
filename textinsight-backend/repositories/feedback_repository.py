from repositories.base_repository import BaseRepository
from django.forms.models import model_to_dict
from typing import List, Dict, Any
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from feedback.models import Feedback
from repositories.assignment_repository import AssignmentRepository

class FeedbackRepository(BaseRepository[Feedback]):
    """
    Initializes the FeedbackRepository class, inheriting from BaseRepository and setting the model to Feedback.
    Initializes the AssignmentRepository for handling related operations.
    """
    def __init__(self):
        super().__init__(Feedback)
        self.assignment_repo = AssignmentRepository()

    """
    Saves feedback data for a user, essay, and assignment.
    Updates the data with the provided information and creates a new feedback entry.
    Returns the saved feedback if successful, otherwise returns False.
    """
    def saveFeedback(self, user_id, essay_id, assignment_id, data):
        try:
            data.update({
                "essay_id": essay_id,
                "assignment_id": assignment_id,
                "student_id": user_id
            })
            
            feedback = self.create(data)

            feedback.calculate_overall_score()
            
            return feedback  

        except ValidationError as e:
            print(f"Validation Error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
    
    """
    Retrieves the inter-essay scores for a specific feedback ID.
    Returns a dictionary containing the scores if found, otherwise returns an empty dictionary.
    """
    def retrieveInterEssayScore(self, feedback_id):
        try:
            feedback = self.model.objects.filter(id=feedback_id).values(
                'originality_score',
                'coherence_score',
                'topic_relevance_score',
                'depth_of_analysis_score',
                'keyword_density_score',
            ).first()  # Access the first result directly as a dictionary

            return feedback if feedback else {}

        except ValidationError as e:
            print(f"Validation Error: {e}")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}

    """
    Retrieves the latest feedback for a specific assignment, excluding the current user's feedback.
    Returns a list of dictionaries containing the feedback data if found, otherwise returns an empty list.
    """
    def get_latest_feedback_for_assignment(self, assignment_id, user_id): 

        try:

            feedbacks = self.model.objects.filter(
                assignment_id = assignment_id
            ).exclude(
                student=user_id
            )

            if not feedbacks.exists():
                raise ObjectDoesNotExist("No feedbacks found for the specified assignment_id.")
            
            latest_feedbacks = (
                feedbacks.order_by('student', '-feedback_date')
            ).distinct('student')


            data = latest_feedbacks.values(
                'id',
                'originality_score',
                'coherence_score',
                'topic_relevance_score',
                'depth_of_analysis_score',
                'keyword_density_score',
            )

            return list(data)
        
        except (ObjectDoesNotExist, ValidationError, Exception):
            return []
        
    """
    Fetches students who do not have inter-essay feedback for a specific assignment.
    Returns a list of dictionaries containing the student IDs if found, otherwise returns an empty list.
    """
    def fetch_students_without_inter_essay_feedback(self, assignment_id):
        try:
            students_without_feedback = self.model.objects.filter(
                assignment_id=assignment_id,
                inter_essay_feedback=""
            ) 

            return list(students_without_feedback.values('id', 'student'))

        except ObjectDoesNotExist:
            return []
        except ValidationError as e:
            print(f"Validation Error: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
    
    """
    Checks if a user has inter-essay feedback for a specific essay and assignment.
    Returns True if the feedback exists, otherwise returns False.
    """
    def check_user_have_inter_essay_feedback(self, user_id, essay_id, assignment_id):
        try:
            return self.model.objects.filter(
                assignment_id=assignment_id,
                student_id=user_id,
                essay_id=essay_id,
            ).exclude(inter_essay_feedback__isnull=True).exclude(inter_essay_feedback="").exists()

        except ValidationError as e:
            print(f"Validation Error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    """
    Retrieves the feedback history for a user.
    Returns a list of dictionaries containing the feedback details if found, otherwise returns an empty list.
    """
    def feedbackHistory(self, user_id):

        try:

            feedbacks = self.model.objects.filter(
                student_id = user_id
            ).order_by('-feedback_date').values_list('id', 'assignment_id', 'feedback_date')

            result = []

            for id, assignment_id, feedback_date in feedbacks:

                assignment = self.assignment_repo.findById(assignment_id)

                result.append({
                    'id': id,
                    'title' : assignment.title,
                    'class_code' : assignment.class_id.class_code,
                    'assignment_id' : assignment_id,
                    "feedback_on": feedback_date.strftime("%d %b %y"),
                })
            

            return result
        
        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
    """
    Retrieves the specific feedback data by feedback ID.
    Returns a dictionary representation of the feedback data if found, otherwise returns None.
    """
    def specficFeedbackdata(self, feedback_id):
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
    Retrieves the specific feedback data for a user by feedback ID.
    Returns a dictionary representation of the feedback data if found, otherwise returns None.
    """
    def specficFeedbackdataOfUser(self,user, feedback_id):
        try:
            data = self.model.objects.get(student_id = user, id=feedback_id) 
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
    Retrieves feedback scores for a given user and assignment, including essay IDs.
    Returns a list of dictionaries containing the five feedback scores and essay ID.
    """
    def get_feedback_scores(self, user_id: int, assignment_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve feedback scores for a given user and assignment, including essay IDs.
        
        Args:
            user_id (int): ID of the user (student).
            assignment_id (int): ID of the assignment.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the five feedback scores and essay ID.
        """
        try:
            feedback_objects = self.model.objects.filter(student_id=user_id, assignment_id=assignment_id)
            
            feedback_scores_list = []
            
            categories = [
                "originality_score", 
                "coherence_score", 
                "topic_relevance_score", 
                "depth_of_analysis_score", 
                "keyword_density_score"
            ]
            
            for feedback in feedback_objects:
                feedback_scores = {category: getattr(feedback, category) for category in categories}
                feedback_scores['essay_id'] = feedback.essay_id  
                feedback_scores_list.append(feedback_scores)
            
            return feedback_scores_list

        except ObjectDoesNotExist:
            print("No feedback found for the specified user and assignment.")
            return []

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    """
    Retrieves the feedback history for the dashboard for a user.
    Returns a list of dictionaries containing the most recent feedback details, limited to the last two submissions.
    Returns an empty list if a ValidationError occurs or if an error occurs.
    """
    def feedbackHistoryDashboard(self, user_id):

        try:

            feedbacks = self.model.objects.filter(
                student_id = user_id
            ).order_by('-feedback_date').values_list('id', 'assignment_id', 'feedback_date')[:2]

            result = []

            for id, assignment_id, feedback_date in feedbacks:

                assignment = self.assignment_repo.findById(assignment_id)

                result.append({
                    'id': id,
                    'title' : assignment.title,
                    'class_code' : assignment.class_id.class_code,
                    "teacher_name": assignment.class_id.teacher_name,
                    'assignment_id' : assignment_id,
                    "feedback_on": feedback_date.strftime("%d %b %y"),
                })
            

            return result
        
        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        
    def get_students_with_feedback(self, assignment_id):
        """
        Fetches the IDs of students who have received feedback for a given assignment.
        Parameters:
            assignment_id: ID of the assignment.
        Returns:
            QuerySet of student IDs and their feedback IDs.
        """
        return self.model.objects.filter(assignment_id=assignment_id).values_list('student_id', 'id', 'feedback_date')