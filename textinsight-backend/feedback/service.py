from business_logic_classes.feedback_class import EssayFeedback
from business_logic_classes.inter_essay_feedback import EssayMetricsCalculator
from repositories.feedback_repository import FeedbackRepository
from business_logic_classes.progess_comparator import ProgressComparator
from repositories.progress_repository import ProgressRepository
from repositories.user_repository import UserRepository

class FeedbackService: 

    # Initializes the FeedbackService with various business logic classes and repositories
    def __init__(self):
        self.intraessay_feedback = EssayFeedback()    
        self.inter_essay_feedback = EssayMetricsCalculator()
        self.feedback_repo = FeedbackRepository()
        self.progress_comparator = ProgressComparator()
        self.progress_repo = ProgressRepository()
        self.user_repo = UserRepository()
    
    """
    Generates intra-essay feedback based on the introduction, middle, and conclusion of the essay
    Use the EssayFeedback class to generate overall feedback for the essay
    """
    def generate_intra_essay_feedback(self, introduction, middle, conclusion):

        return self.intraessay_feedback.generate_overall_feedback(introduction, middle, conclusion)
    
    """
    Generates inter-essay scores based on the essay text and expected keywords
    Use the EssayMetricsCalculator class to calculate all scores for the essay
    """
    def generate_inter_essay_score(self, essay, keywords):

        return self.inter_essay_feedback.calculate_all_scores(essay, keywords)
    
    """
    Generates inter-essay feedback by comparing the user's feedback score with the class feedback score
    Use the EssayMetricsCalculator class to compare the user's feedback with the class feedback
    """
    def generate_inter_essay_feedback(self, feedback_score, user_feedback_score):

        return self.inter_essay_feedback.compare_user_with_class(feedback_score, user_feedback_score)
    
    """
    Fetches the feedback history for a specific user
    Fetch and return the feedback history from the repository
    Handle any exceptions and return an empty list if an error occurs
    """
    def get_feedback_history(self, user_id):
        try:

            return self.feedback_repo.feedbackHistory(user_id)

        except Exception as e:
            print(f"An error occurred while fetching feedback history: {e}")
            return []  

    """
    Fetches the details of a specific feedback entry
    Fetch and return the specific feedback data from the repository
    Handle any exceptions and return None if an error occurs
    """
    def get_feedback(self,user_id, feedback_id):

        try:

            data = self.feedback_repo.specficFeedbackdataOfUser(user_id, feedback_id)

            if data:
                return data
            else:
                return None

        except Exception as e:
            print(f"An error occurred while fetching feedback data: {e}")
            return None

    """
    Generates progress data by comparing two essay submissions
    Use the ProgressComparator class to compare the two submissions
    Create a progress entry in the repository with the comparison data
    """
    def generate_progress(self, user_id, assignment_id, essay1_id, essay2_id, submission_1, submission_2):

        data = self.progress_comparator.compare_submissions(submission_1, submission_2)

        self.progress_repo.create(
            {
                "student" : user_id,
                "essay_1_id" : essay1_id,
                "essay_2_id" : essay2_id,
                "assignment_id" : assignment_id,
                **data
            }
        )

    """
    Fetches the progress history for a specific user
    Fetch and return the progress history from the repository
    Handle any exceptions and return an empty list if an error occurs
    """
    def get_progress_history(self, user_id):
        try:

            return self.progress_repo.progressHistory(user_id)

        except Exception as e:
            print(f"An error occurred while fetching progress history: {e}")
            return []  

    """
    Fetches the details of a specific progress entry
    Fetch and return the specific progress data from the repository
    Handle any exceptions and return None if an error occurs
    """
    def get_progress(self,user_id, feedback_id):

        try:

            data = self.progress_repo.specficProgressDataOfUser(user_id, feedback_id)
            
            if data:
                return data
            else:
                return None

        except Exception as e:
            print(f"An error occurred while fetching progress data: {e}")
            return None

    """
    Fetches the feedback history for the dashboard
    Fetch and return the feedback history from the repository for the dashboard
    Handle any exceptions and return an empty list if an error occurs
    """
    def getFeedbackHistoryDashboard(self, user_id):
        try:

            return self.feedback_repo.feedbackHistoryDashboard(user_id)

        except Exception as e:
            print(f"An error occurred while fetching feedback history: {e}")
            return [] 

    """
    Fetches the progress history for the dashboard
    Fetch and return the progress history from the repository for the dashboard
    Handle any exceptions and return an empty list if an error occurs
    """
    def getProgressHistoryDashboard(self, user_id):
        try:

            return self.progress_repo.progressHistoryDashboard(user_id)

        except Exception as e:
            print(f"An error occurred while fetching progress history: {e}")
            return []  


    def fetch_feedback_details(self, assignment_id):
        """
        Fetches feedback details for students in a specific assignment.
        Parameters:
            assignment_id: ID of the assignment.
        Returns:
            List of feedback details with student name, feedback ID, and feedback date.
        """
        # Step 1: Fetch students and their feedback IDs
        feedback_records = self.feedback_repo.get_students_with_feedback(assignment_id)
        if not feedback_records:
            return []

        # Extract student IDs and feedback details
        student_ids = [record[0] for record in feedback_records]
        feedback_mapping = {record[0]: {"feedback_id": record[1], "feedback_date": record[2]} for record in feedback_records}

        # Step 2: Fetch user details
        students = self.user_repo.find_by_ids(student_ids)

        # Step 3: Combine data
        feedback_details = [
            {
                "id": student.id,
                "name": student.name,
                "feedback_id": feedback_mapping[student.id]["feedback_id"],
                "feedback_on": feedback_mapping[student.id]["feedback_date"].strftime("%d %b %y")
            }
            for student in students
        ]

        return feedback_details
    
    def get_feedback_details(self, student_id, feedback_id):
        """
        Fetch specific feedback data for a given student and feedback ID.
        """
        feedback_data = self.feedback_repo.specficFeedbackdataOfUser(student_id, feedback_id)
        if not feedback_data:
            return None

        return feedback_data
    
    def fetch_progress_details(self, assignment_id):
        """
        Fetches progress details for students in a specific assignment.
        Parameters:
            assignment_id: ID of the assignment.
        Returns:
            List of progress details with student name, progress ID, and progress date.
        """
        # Step 1: Fetch students and their progress IDs
        progress_records = self.progress_repo.get_students_with_progress(assignment_id)
        if not progress_records:
            return []

        # Extract student IDs and progress details
        student_ids = [record[0] for record in progress_records]
        progress_mapping = {record[0]: {"progress_id": record[1], "progress_date": record[2]} for record in progress_records}

        # Step 2: Fetch user details
        students = self.user_repo.find_by_ids(student_ids)

        # Step 3: Combine data
        progress_details = [
            {
                "id": student.id,
                "name": student.name,
                "progress_id": progress_mapping[student.id]["progress_id"],
                "progress_on": progress_mapping[student.id]["progress_date"].strftime("%d %b %y")
            }
            for student in students
        ]

        return progress_details
    
    def get_progress_details(self, student_id, progress_id):
        """
        Fetch specific progress data for a given student and progress ID.
        """
        progress_data = self.progress_repo.specficProgressDataOfUser(student_id, progress_id)
        if not progress_data:
            return None

        return progress_data