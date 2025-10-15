from django.db import models
from essay.models import Essay, Assignment
from authentication.models import User

class Feedback(models.Model):
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE, related_name='feedback') 
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')  
    assignment = models.ForeignKey(Assignment, default=1, on_delete=models.CASCADE, related_name='assignment_feedback')

    intra_essay_feedback = models.TextField()
    inter_essay_feedback = models.TextField()

    keywords = models.JSONField(default=list)
    intro_keywords = models.JSONField(default=list)
    middle_keywords = models.JSONField(default=list)
    conclusion_keywords = models.JSONField(default=list)
    intro_mid_keywords = models.JSONField(default=list)
    intro_conclusion_keywords = models.JSONField(default=list)
    mid_conclusion_keywords = models.JSONField(default=list)
    intro_mid_conclusion_keywords = models.JSONField(default=list)
    
    wordcloud_image = models.CharField(max_length=500, blank=True)
    venn_diagram_image = models.CharField(max_length=500, blank=True)
    radar_wheel_image = models.CharField(max_length=500, blank=True)
    keyword_graph_html = models.TextField(blank=True)

    originality_score = models.IntegerField(default=0)  
    coherence_score = models.IntegerField(default=0)    
    topic_relevance_score = models.IntegerField(default=0) 
    depth_of_analysis_score = models.IntegerField(default=0) 
    keyword_density_score = models.IntegerField(default=0)   

    overall_score = models.IntegerField(default=0)   
    feedback_date = models.DateTimeField(auto_now_add=True)
    teacher_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Feedback for {self.essay.title} by {self.student.username}"

    def calculate_overall_score(self):
        total_score = (
            self.originality_score +
            self.coherence_score +
            self.topic_relevance_score +
            self.depth_of_analysis_score +
            self.keyword_density_score
        )
        self.overall_score = total_score // 5
        self.save()

class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress') 
    essay_1 = models.ForeignKey(Essay, on_delete=models.CASCADE, related_name='first_essay')  
    essay_2 = models.ForeignKey(Essay, on_delete=models.CASCADE, related_name='second_essay')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignment_progress')
    graph_image = models.CharField(max_length=500 )
    compared_feedback = models.TextField(max_length=500)
    progress_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Progress for {self.student.username} between submissions"
