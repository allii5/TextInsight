from repositories.class_repository import ClassRepository, ClassStudentsRepository
from repositories.assignment_repository import AssignmentRepository
from repositories.essay_repository import EssayRepository
from repositories.feedback_repository import FeedbackRepository
from business_logic_classes.keyword_extraction_algorithm import Algorithm
from feedback.service import FeedbackService
from concurrent.futures import ThreadPoolExecutor
from repositories.user_repository import UserRepository
from repositories.notification_repository import NotificationRepository
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from custom_error_classes import AssignmentNotFoundError, DueDatePassedError, FeedbackNotAvailableError, UserNotInClassError, SubmissionLimitExceededError
import logging

logging.basicConfig(level=logging.ERROR)

class EssayService:
    # Initializes the EssayService with various repositories and services
    def __init__(self):
        self.class_repository = ClassRepository()
        self.class_students_repository = ClassStudentsRepository()
        self.assignment_repository = AssignmentRepository()
        self.essay_repository = EssayRepository()
        self.keyword_extraction_algorithm = Algorithm()
        self.feedback_service = FeedbackService()
        self.feedback_repository = FeedbackRepository()
        self.user_repository = UserRepository()
        self.notification_repository = NotificationRepository()

    """
    Fetches the list of pending assignments for the authenticated student
    Fetch class IDs for the student
    Fetch assignments for the class IDs
    Fetch essay submissions for the student and assignment IDs
    Return the list of pending assignments
    """
    def fetchListOfPendingAssignment(self, user: str):
        try:
            class_ids = self.class_students_repository.findByStudentId(user)

            if not class_ids:
                return []

            assignments = self.assignment_repository.findByClassId(class_ids)

            assignment_ids = [assignment["assignment_id"] for assignment in assignments]

            if not assignment_ids:
                return []

            essay_submission_with_assignment = self.essay_repository.findByStudentIdAndAssignmentId(user, assignment_ids)
            
            return essay_submission_with_assignment

        except Exception as e:
            print(f"An error occurred while fetching pending assignments: {e}")
            return [] 

    """
    Submits an essay for the authenticated student
    Generate essay text from introduction, middle, and conclusion
    Save the essay submission
    Generate feedback data
    Update the essay status and notify the user
    Save feedback and generate progress analysis if applicable
    Return the feedback data 
    """
    def submitEssay(self, user, assignment_id, introduction, middle, conclusion):
        try:
            essay_text = self._generate_essay_text(introduction, middle, conclusion)
            essay_title = self.assignment_repository.titleById(assignment_id)
            essay = self.essay_repository.save_submission(assignment_id, user, essay_text)

            keywords = self.assignment_repository.Expected_keywordsById(assignment_id)
            feedback_data = self._generate_feedback_data(introduction, middle, conclusion, essay_text, keywords)

            self.essay_repository.updateById(essay.id, {"status": "reviewed"})
            self._notify_user(user.id, essay_title, "Intra Essay Feedback")

            feedback = self.feedback_repository.saveFeedback(user.id, essay.id, assignment_id, feedback_data)

            scores = self.feedback_repository.retrieveInterEssayScore(feedback.id)
            self._generate_class_inter_essay_feedback(assignment_id, user, scores, essay_title)

            feedback_scores = self.feedback_repository.get_feedback_scores(user.id, assignment_id)
            if len(feedback_scores) == 2:
                first_submission_scores = {key: value for key, value in feedback_scores[0].items() if key != "essay_id"}
                second_submission_scores = {key: value for key, value in feedback_scores[1].items() if key != "essay_id"}
                first_essay_id = feedback_scores[0].get("essay_id")
                second_essay_id = feedback_scores[1].get("essay_id")

                self.feedback_service.generate_progress(user, assignment_id, first_essay_id, second_essay_id, 
                                                        first_submission_scores, second_submission_scores)
                self._notify_user(user.id, essay_title, "Progress Analysis")

            return feedback_data

        except (AssignmentNotFoundError, DueDatePassedError, UserNotInClassError, 
                FeedbackNotAvailableError, SubmissionLimitExceededError) as e:
            logging.error(f"Validation error in submitEssay: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in submitEssay: {str(e)}", exc_info=True)
            raise
    
    """
    Generates the full text of the essay from its parts
    Concatenate introduction, middle, and conclusion to form the full essay text
    """
    def _generate_essay_text(self, introduction, middle, conclusion):
        try:
            return f"{introduction} {middle} {conclusion}"
        except Exception as e:
            print(f"Error generating essay text: {e}")
            return None

    """
    Generates feedback data for the essay submission
    Use ThreadPoolExecutor to concurrently generate keyword extraction, intra-essay feedback, and inter-essay score
    Combine the results into feedback data
    """
    def _generate_feedback_data(self, introduction, middle, conclusion, essay_text, keywords):
        try:
            with ThreadPoolExecutor() as executor:
                keyword_extraction_future = executor.submit(self.keyword_extraction_algorithm.do_all_working, introduction, middle, conclusion)
                intra_essay_feedback_future = executor.submit(self.feedback_service.generate_intra_essay_feedback, introduction, middle, conclusion)
                inter_essay_score_future = executor.submit(self.feedback_service.generate_inter_essay_score, essay_text, keywords)

                feedback_data = {
                    **keyword_extraction_future.result(),
                    'intra_essay_feedback': intra_essay_feedback_future.result(),
                    **inter_essay_score_future.result()  
                }

            return feedback_data

        except Exception as e:
            print(f"Error generating feedback data: {e}")
            return None

    """
    Notifies the user about the feedback generation
    Create a notification message
    Update the user's notifications
    """
    def _notify_user(self, user, essay_title, feedback_type):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"{feedback_type} has been successfully generated for {essay_title} at {timestamp}."
            notification = self.notification_repository.create({"message": message})
            
            self.user_repository.updateById(user, {"notifications": [notification.id]})

        except Exception as e:
            print(f"Error notifying user {user.id} for {feedback_type}: {e}")

    """
    Generates inter-essay feedback for the class
    Fetch the latest feedback for the assignment
    Generate inter-essay feedback if there are enough submissions
    Update the essay feedback and notify the user
    Generate feedback for remaining students
    """
    def _generate_class_inter_essay_feedback(self, assignment_id, user, inter_essay_score, essay_title):
        try:
            rest_of_class_feedback = self.feedback_repository.get_latest_feedback_for_assignment(assignment_id, user.id)

            if len(rest_of_class_feedback) > 5:


                feedback_data = self.feedback_service.generate_inter_essay_feedback(rest_of_class_feedback, inter_essay_score)
                self._update_essay_feedback(user.id, feedback_data)

                self._notify_user(user.id, essay_title, "Inter Essay Feedback")

                self._generate_feedback_for_remaining_students(assignment_id, essay_title)

        except Exception as e:
            print(f"Error generating class inter-essay feedback for assignment {assignment_id}: {e}")

    """
    Updates the essay feedback with inter-essay feedback data
    Update the essay feedback in the repository
    """
    def _update_essay_feedback(self, id, feedback_data):
        try:
            update_data = {
                "inter_essay_feedback": feedback_data["inter_essay_feedback"],
                "radar_wheel_image": feedback_data["radar_chart_img"]
            }
            self.feedback_repository.updateById(id, update_data)

        except Exception as e:
            print(f"Error updating essay feedback for user {id}: {e}")

    """
    Generates inter-essay feedback for remaining students in the class
    Fetch students without inter-essay feedback
    Generate and update feedback for each student
    Notify each student
    """
    def _generate_feedback_for_remaining_students(self, assignment_id, essay_title):
        try:
            students_without_feedback = self.feedback_repository.fetch_students_without_inter_essay_feedback(assignment_id)


            for student in students_without_feedback:

                rest_of_class_feedback = self.feedback_repository.get_latest_feedback_for_assignment(assignment_id, student['student'])
                inter_essay_score = self.feedback_repository.retrieveInterEssayScore(student['id'])
                feedback_data = self.feedback_service.generate_inter_essay_feedback(rest_of_class_feedback, inter_essay_score)

                self._update_essay_feedback(student['id'], feedback_data)

                self._notify_user(student['student'], essay_title, "Inter Essay Feedback")

        except Exception as e:
            print(f"Error generating feedback for remaining students in assignment {assignment_id}: {e}")  

    """
    Fetches the submission history for the authenticated student
    Fetch and return the submission history from the repository
    """
    def get_submission_history(self, user_id):
        try:

            return self.essay_repository.submissionHistory(user_id) 

        except Exception as e:
            print(f"An error occurred while fetching submission history: {e}")
            return []  

    """
    Fetches the content of a specific submission
    Fetch and return the content of the specified submission from the repository
    """
    def get_submission_content(self, user_id, submission_id):

        try:
            data = self.essay_repository.specificSubmissionContentOfUser(user_id, submission_id)

            if data:
                return data
            else:
                return None

        except Exception as e:
            print(f"An error occurred while fetching submission content: {e}")
            return None

    """
    Fetches the list of pending assignments for the dashboard
    Fetch class IDs for the student
    Fetch assignments for the class IDs
    Fetch essay submissions for the student and assignment IDs
    Return the list of pending assignments for the dashboard
    """
    def fetchPendingAssignmentDashboard(self, user: str):
        try:
            class_ids = self.class_students_repository.findByStudentId(user)

            if not class_ids:
                return []

            assignments = self.assignment_repository.findByClassId(class_ids)

            assignment_ids = [assignment["assignment_id"] for assignment in assignments]

            if not assignment_ids:
                return []

            essay_submission_with_assignment = self.essay_repository.findByStudentIdAndAssignmentIdDashboard(user, assignment_ids)
            
            return essay_submission_with_assignment

        except Exception as e:
            print(f"An error occurred while fetching pending assignments: {e}")
            return []  
    
    """
    Fetches the submission history for the dashboard
    Fetch and return the submission history from the repository for the dashboard
    """
    def getSubmissionHistoryDashboard(self, user_id):
        try:

            return self.essay_repository.submissionHistoryDashboard(user_id) 

        except Exception as e:
            print(f"An error occurred while fetching submission history: {e}")
            return []  

    """
    Fetches the notification history for the authenticated student
    Fetch and return the unread notifications from the repository
    SHOULD BE IN AUTHENTICATION APP
    """
    def get_notification_history(self, user_id):
        try:

            return self.user_repository.fetch_unread_notifications(user_id)

        except Exception as e:
            print(f"An error occurred while fetching notification history: {e}")
            return []  
    
    """
    Compiles data for the dashboard
    Fetch pending assignments, feedback history, progress history, and submission history for the dashboard
    Compile all data into a single dictionary and return it
    SHOULD BE IN AUTHENTICATION APP
    """
    def dashboardData(self, user_id):
        try:
            # Fetch pending assignments for the dashboard
            pending_assignments = self.fetchPendingAssignmentDashboard(user_id)
            
            # Fetch feedback history for the dashboard
            feedback_history = self.feedback_service.getFeedbackHistoryDashboard(user_id)
            
            # Fetch progress history for the dashboard
            progress_history = self.feedback_service.getProgressHistoryDashboard(user_id)
            
            # Fetch submission history for the dashboard
            submission_history = self.getSubmissionHistoryDashboard(user_id)

            # Compile all data into a single dictionary
            dashboard_data = {
                "pending_assignments": pending_assignments,
                "feedback_history": feedback_history,
                "progress_history": progress_history,
                "submission_history": submission_history
            }

            return dashboard_data

        except Exception as e:
            print(f"An error occurred while fetching dashboard data: {e}")
            return {
                "pending_assignments": [],
                "feedback_history": [],
                "progress_history": [],
                "submission_history": []
            }
    
    def fetch_students_submission_data(self, assignment_id):
        """
        Fetches student submission details for a given assignment.
        Parameters:
            assignment_id: ID of the assignment.
        Returns:
            List of dictionaries containing student ID, name, and submission date.
        """
        # Fetch essays for the assignment
        essays = self.essay_repository.get_students_who_submitted_essays(assignment_id)
        if not essays.exists():
            return []

        # Extract student IDs
        student_ids = [essay.student.id for essay in essays]

        # Fetch student details
        students = self.user_repository.find_by_ids(student_ids)

        # Format the response
        student_data = [
            {
                "id": essay.student.id,
                "name": essay.student.name, 
                "submission_id": essay.id,
                "submission_on": essay.submission_date.strftime("%d %b %y"),
            }
            for essay in essays
        ]

        return student_data

    def fetch_student_submission_content(self, student_id, submission_id):
        """
        Fetch specific submission content for a student.
        """
        content = self.essay_repository.specificSubmissionContentOfUser(user=student_id, submission_id=submission_id)
        if not content:
            raise ValueError("No submission found for the given student and submission ID.")
        return content

    def get_teacher_dashboard(self, teacher_id):
        # Validate teacher_id
        if not teacher_id:
            raise ValueError("teacher_id cannot be None or empty.")

        # Fetch teacher's classes
        teacher_classes = self.class_repository.get_teacher_classes(teacher_id)
        if not teacher_classes:
            return {
                "manage_classes": [],
                "manage_essays": [],
                "submission_history": [],
                "feedback_history": [],
                "progress_monitoring": [],
            }

        # Extract class IDs
        class_ids = [cls.id for cls in teacher_classes]

        # Fetch assignments for these class IDs
        assignments = self.assignment_repository.get_assignments_by_class_ids_dashbaord(class_ids)

        # Format assignments
        formatted_assignments = [
            {
                "id": assignment.id,
                "title": assignment.title,
                "class_code": assignment.class_id.class_code if assignment.class_id else None,
                "deadline": assignment.due_date.strftime("%d %b %y"),
            }
            for assignment in assignments
        ] if assignments else []

        # Fetch limited classes for dashboard
        limited_classes = self.class_repository.get_teacher_classes_dashboard(teacher_id)

        # Format classes
        formatted_classes = [
            {
                "id": cls.id,
                "class_name": cls.class_name,
                "class_code": cls.class_code,
                "student_count": cls.student_count,
                "student_limit": cls.student_limit,
                "created" : cls.created_at.strftime("%d %b %y")
            }
            for cls in limited_classes
        ] if limited_classes else []

        # Construct the dashboard response
        return {
            "manage_classes": formatted_classes,
            "manage_essays": formatted_assignments,
            "submission_history": formatted_assignments,
            "feedback_history": formatted_assignments,
            "progress_monitoring": formatted_assignments
        }


class AssignmentService:
    def __init__(self):
        self.assignment_repo = AssignmentRepository()
        self.class_repo = ClassRepository()

    def create_assignment(self, teacher_id, data):
        """
        Handles essay assignment creation with validation.
        """
        try:
            # Extract data fields
            title = data.get('title')
            description = data.get('description')
            class_id = data.get('class_id')
            due_date = data.get('due_date')
            expected_keywords = data.get('expected_keywords')

            # Validate Class Ownership
            teacher_classes = self.class_repo.get_classes_by_teacher(teacher_id)

            if class_id not in [(cls.id) for cls in teacher_classes]:
                raise ValidationError({'class_id': 'You can only assign essays to your own classes.'})
            

            # Step 4: Create Assignment
            assignment_data = {
                'title': title,
                'description': description,
                'class_id_id': class_id,
                'expected_keywords': expected_keywords,
                'due_date': due_date
            }
            assignment = self.assignment_repo.create(assignment_data)

            return {
                'status': 'success',
                'message': 'Assignment created successfully.',
                'assignment_id': assignment.id
            }

        except ValidationError as e:
            return {'status': 'error', 'errors': e.message_dict}
        except Exception as e:
            print(f"Unexpected error during assignment creation: {e}")
            return {'status': 'error', 'message': 'An unexpected error occurred.'}
    
    def update_assignment(self, teacher_id, data):
        """
        Handles essay assignment updation with validation.
        """
        try:
            # Extract data fields
            title = data.get('title')
            description = data.get('description')
            assignment_id = data.get('assignment_id')
            class_id = data.get('class_id')
            due_date = data.get('due_date')
            expected_keywords = data.get('expected_keywords')

            assignment_exists = self.assignment_repo.exists_by_id_and_class(assignment_id, class_id)
            
            if not assignment_exists:
                raise ValidationError({'assignment id': 'No assignment found for the given class.'})


            # Validate Class Ownership
            teacher_classes = self.class_repo.get_classes_by_teacher(teacher_id)
            if class_id not in [(cls.id) for cls in teacher_classes]:
                raise ValidationError({'class_id': 'You can only assign essays to your own classes.'})
            
            # Step 4: update Assignment
            assignment_data = {
                'title': title,
                'description': description,
                'class_id_id': class_id,
                'expected_keywords': expected_keywords,
                'due_date': due_date
            }
            self.assignment_repo.updateById(assignment_id,assignment_data)

            return {
                'status': 'success',
                'message': 'Assignment updated successfully.',
                'assignment_id': assignment_id
            }

        except ValidationError as e:
            return {'status': 'error', 'errors': e.message_dict}
        except Exception as e:
            print(f"Unexpected error during assignment update: {e}")
            return {'status': 'error', 'message': 'An unexpected error occurred.'}
    
    def get_teacher_assignments(self, teacher_id):
        # Step 1: Fetch classes of the teacher
        classes = self.class_repo.get_teacher_classes(teacher_id)
        if not classes:
            return []
        class_ids = [cls.id for cls in classes]

        # Step 2: Fetch assignments for these classes
        assignments = self.assignment_repo.get_assignments_by_class_ids(class_ids)
        if not assignments:
            return []

        # Step 3: Format data
        formatted_assignments = [
            {
                "id": assignment.id,
                "title": assignment.title,
                "class_code": assignment.class_id.class_code,
                "deadline": assignment.due_date.strftime("%d %b %y")
            }
            for assignment in assignments
        ]

        return formatted_assignments
    
    def get_assignment_details(self, assignment_id):
        # Step 1: Fetch assignment details
        assignment = self.assignment_repo.get_assignment_by_id(assignment_id)
        if not assignment:
            return None

        # Step 2: Format data
        formatted_assignment = {
            "id": assignment.id,
            "title": assignment.title,
            "description": assignment.description,
            "class_id": assignment.class_id.id,
            "due_date": assignment.due_date.strftime("%Y-%m-%d"),
            "expected_keywords": assignment.expected_keywords
        }

        return formatted_assignment
