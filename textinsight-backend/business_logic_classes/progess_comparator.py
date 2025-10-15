import os
import time
import matplotlib.pyplot as plt
import numpy as np

class ProgressComparator:
    """
    Initializes the ProgressComparator class with the output directory for saving generated results.
    Creates the output directory if it does not exist.
    """
    def __init__(self):
        self.output_dir = "static/generated_result/"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    """
    Compares two submissions based on their scores in various categories.
    Generates a bar chart and HTML feedback comparing the scores of the two submissions.
    Returns the paths to the generated bar chart and the HTML feedback.
    """
    def compare_submissions(self, first_submission_scores, second_submission_scores):
        categories = [
            "originality_score", 
            "coherence_score", 
            "topic_relevance_score", 
            "depth_of_analysis_score", 
            "keyword_density_score"
        ]

        first_scores = [first_submission_scores[category] for category in categories]
        second_scores = [second_submission_scores[category] for category in categories]
        
        bar_chart_path = self.generate_bar_chart(categories, first_scores, second_scores)
        html_feedback = self.generate_html_feedback(categories, first_scores, second_scores)

        return {"graph_image": bar_chart_path, "compared_feedback": html_feedback}

    """
    Generates a bar chart comparing the scores of the two submissions.
    Plots the scores for each category side by side for easy comparison.
    Saves the bar chart as an image file and returns the path to the saved image.
    """
    def generate_bar_chart(self, categories, first_scores, second_scores):
        x = np.arange(len(categories))  
        width = 0.35  

        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.bar(x - width/2, first_scores, width, label='First Submission', color='skyblue')
        ax.bar(x + width/2, second_scores, width, label='Second Submission', color='salmon')
        
        ax.set_xlabel('Score Categories')
        ax.set_ylabel('Scores')
        ax.set_title('Comparison of First and Second Submissions')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45)
        ax.legend(loc='upper left')

        for i in range(len(categories)):
            ax.text(i - width / 2, first_scores[i] + 0.1, str(first_scores[i]), ha='center', color='blue')
            ax.text(i + width / 2, second_scores[i] + 0.1, str(second_scores[i]), ha='center', color='red')

        timestamp = str(int(time.time()))
        bar_chart_path = os.path.join(self.output_dir, f"bar_chart_{timestamp}.png")
        plt.savefig(bar_chart_path, format="png", bbox_inches="tight")
        plt.close(fig)

        return f"/{bar_chart_path}"
    
    """
    Generates HTML feedback comparing the scores of the two submissions.
    Provides detailed suggestions for improvement based on the comparison.
    Returns the HTML feedback as a string.
    """
    def generate_html_feedback(self, categories, first_scores, second_scores):
        feedback_html = "<h2>Progress Feedback</h2><p>Below is an analysis of your progress between the two submissions, along with detailed suggestions for each category:</p>"
        feedback_html += "<ul>"

        for i, category in enumerate(categories):
            first_score = first_scores[i]
            second_score = second_scores[i]
            improvement = second_score - first_score

            if second_score <= 5:
                score_quality = "poor"
            elif 6 <= second_score <= 8:
                score_quality = "average"
            else:
                score_quality = "strong"

            feedback_html += f"<li><strong>{category.replace('_', ' ').capitalize()}:</strong> "

            if category == "originality_score":
                if improvement > 0:
                    feedback_html += "There's a noticeable improvement in originality. "
                    if score_quality == "poor":
                        feedback_html += "You might try incorporating fresh perspectives and unique viewpoints that go beyond standard ideas to make your work stand out more."
                    elif score_quality == "average":
                        feedback_html += "You’re developing originality well! You might continue to build on distinctive ideas and ensure your points are less commonly expressed."
                    else:
                        feedback_html += "Fantastic work on originality! You might keep pushing for unique ideas and arguments to enhance the impact of your writing."
                elif improvement < 0:
                    feedback_html += "Your originality has decreased since the last submission. "
                    if score_quality == "poor":
                        feedback_html += "You might focus on bringing in new ideas or exploring the topic from a different angle to enhance originality."
                    elif score_quality == "average":
                        feedback_html += "You might want to add unique insights that make your points more memorable and distinct."
                    else:
                        feedback_html += "You might aim to maintain your unique ideas to keep the content engaging and original."
                else:
                    feedback_html += "Originality has remained consistent. You might enhance it by adding unique insights or novel perspectives."

            elif category == "coherence_score":
                if improvement > 0:
                    feedback_html += "Your essay’s coherence has improved. "
                    if score_quality == "poor":
                        feedback_html += "You might focus on creating clear, logical connections between paragraphs, using smooth transitions to ensure each idea flows naturally into the next."
                    elif score_quality == "average":
                        feedback_html += "The flow of ideas is clearer. You might continue strengthening the connections between sentences and paragraphs for even greater coherence."
                    else:
                        feedback_html += "Your essay’s flow is well-structured. You might keep refining transitions to maintain smooth readability."
                elif improvement < 0:
                    feedback_html += "There’s been a decline in coherence. "
                    if score_quality == "poor":
                        feedback_html += "You might work on organizing your ideas better, perhaps using linking words and structuring paragraphs to enhance the flow of ideas."
                    elif score_quality == "average":
                        feedback_html += "You might consider using clear transitions between ideas to reinforce coherence in your arguments."
                    else:
                        feedback_html += "You might aim to maintain coherence by carefully structuring each section to enhance readability."
                else:
                    feedback_html += "Coherence has remained stable. You might keep focusing on logical transitions and well-structured paragraphs."

            elif category == "topic_relevance_score":
                if improvement > 0:
                    feedback_html += "Your content relevance has improved significantly. "
                    if score_quality == "poor":
                        feedback_html += "You might continue linking your arguments and examples to the main topic to strengthen the overall alignment."
                    elif score_quality == "average":
                        feedback_html += "You’re better aligned with the topic. You might keep refining your content to ensure everything is highly relevant."
                    else:
                        feedback_html += "Your essay demonstrates excellent topic relevance. You might ensure examples remain strongly connected to the central theme."
                elif improvement < 0:
                    feedback_html += "Relevance to the topic has decreased. "
                    if score_quality == "poor":
                        feedback_html += "You might focus on staying on topic throughout, ensuring every point relates to the main subject."
                    elif score_quality == "average":
                        feedback_html += "You might try refining your arguments to enhance alignment with the core topic."
                    else:
                        feedback_html += "You might reassess certain points to maintain strong alignment with the topic."
                else:
                    feedback_html += "Topic relevance has remained steady. You might enhance relevance by closely linking each section to the main theme."

            elif category == "depth_of_analysis_score":
                if improvement > 0:
                    feedback_html += "There’s a noticeable improvement in analysis depth. "
                    if score_quality == "poor":
                        feedback_html += "You might consider expanding on key points by analyzing underlying causes or implications to deepen understanding."
                    elif score_quality == "average":
                        feedback_html += "You’re building more in-depth analysis. You might focus on examining different aspects to add further depth to your arguments."
                    else:
                        feedback_html += "Your analysis is highly insightful. You might continue developing detailed arguments to maintain depth."
                elif improvement < 0:
                    feedback_html += "There’s been a decline in analysis depth. "
                    if score_quality == "poor":
                        feedback_html += "You might try exploring your arguments further by considering ‘why’ and ‘how’ questions to add layers to your analysis."
                    elif score_quality == "average":
                        feedback_html += "You might strengthen your analysis by delving deeper into key arguments."
                    else:
                        feedback_html += "You might aim to maintain a high level of depth by thoroughly examining your arguments and evidence."
                else:
                    feedback_html += "Depth of analysis has remained stable. You might add more detailed exploration of points to improve it."

            elif category == "keyword_density_score":
                if improvement > 0:
                    feedback_html += "There’s an improvement in keyword usage. "
                    if score_quality == "poor":
                        feedback_html += "You might consider using keywords to clarify your essay’s focus, while avoiding overuse."
                    elif score_quality == "average":
                        feedback_html += "Your keyword usage is more effective. You might aim to integrate them naturally to enhance relevance."
                    else:
                        feedback_html += "You have a balanced approach to keywords. You might continue ensuring natural use to strengthen topic focus."
                elif improvement < 0:
                    feedback_html += "There’s a decrease in keyword usage. "
                    if score_quality == "poor":
                        feedback_html += "You might ensure keywords are present to reinforce the essay’s central themes, but be mindful of excessive repetition."
                    elif score_quality == "average":
                        feedback_html += "You might refocus on using relevant keywords to maintain the connection with the main topic."
                    else:
                        feedback_html += "You might aim to maintain appropriate keyword usage to support the essay’s focus and cohesion."
                else:
                    feedback_html += "Keyword density has remained stable. You might aim for natural integration of keywords to keep the essay focused."

            feedback_html += "</li>"

        feedback_html += "</ul><p>The bar chart visually represents your progress between submissions. A taller bar in the second submission signifies improvement in that category.</p>"
        return feedback_html

