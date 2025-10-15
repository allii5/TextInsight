import nltk
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from statistics import mean
from media.service import MediaService

class EssayMetricsCalculator:

    """
    Initializes the EssayMetricsCalculator class with the SentenceTransformer model and MediaService.
    Load the SentenceTransformer model for generating sentence embeddings.
    Initialize the MediaService for saving media files.
    """
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.media_service = MediaService()

    """
    Calculates the originality score of the essay based on the diversity of words used.
    Tokenize the essay text into words and calculate the diversity ratio.
    The diversity ratio is the number of unique words divided by the total number of words.
    The originality score is scaled to a range of 0 to 10.
    Return the originality score.
    """
    def calculate_originality(self, essay_text):
       
        words = nltk.word_tokenize(essay_text.lower())
        unique_words = set(words)
        diversity_ratio = len(unique_words) / len(words) if words else 0
        
        originality_score = diversity_ratio * 10
        return float(max(0, min(10, originality_score)))

    """
    Calculates the coherence score of the essay based on the similarity between consecutive sentences.
    Tokenize the essay text into sentences.
    If there are fewer than 2 sentences, return a perfect coherence score of 10.
    Encode each sentence to generate embeddings.
    Calculate the cosine similarity between consecutive sentence embeddings.
    Compute the average coherence score and scale it to a range of 0 to 10.
    Return the coherence score.
    """
    def calculate_coherence(self, essay_text):
         
        sentences = nltk.sent_tokenize(essay_text)
        
        if len(sentences) < 2:
            return 10.0  

        sentence_embeddings = [self.model.encode(sentence, convert_to_tensor=True) for sentence in sentences]

        coherence_scores = [
            util.pytorch_cos_sim(sentence_embeddings[i], sentence_embeddings[i + 1]).item()
            for i in range(len(sentence_embeddings) - 1)
        ]
        
        avg_coherence = np.mean(coherence_scores)
        coherence_score = avg_coherence * 10  

        return float(max(0, min(10, coherence_score)))

    """
    Calculates the topic relevance score of the essay based on the presence of topic-specific keywords.
    If no topic keywords are provided, return a perfect relevance score of 10.
    Tokenize the essay text into words.
    Count the number of matched keywords in the essay text.
    Calculate the relevance ratio as the number of matched keywords divided by the total number of topic keywords.
    The relevance score is scaled to a range of 0 to 10.
    Return the relevance score.
    """
    def calculate_topic_relevance(self, essay_text, topic_keywords):
       
        if not topic_keywords:
            return 10.0  

        words = nltk.word_tokenize(essay_text.lower())
        matched_keywords = sum(1 for word in words if word in topic_keywords)
        relevance_ratio = matched_keywords / len(topic_keywords)

        relevance_score = relevance_ratio * 10  
        return float(max(0, min(10, relevance_score)))

    """
    Calculates the depth of analysis score of the essay based on the average sentence length.
    Tokenize the essay text into sentences.
    Calculate the word count for each sentence.
    Compute the average sentence length.
    The depth score is scaled to a range of 0 to 10 based on the average sentence length.
    Return the depth score.
    """
    def calculate_depth_of_analysis(self, essay_text):
        
        sentences = nltk.sent_tokenize(essay_text)
        word_counts = [len(nltk.word_tokenize(sentence)) for sentence in sentences]
        avg_sentence_length = np.mean(word_counts)

        
        depth_score = min(10, avg_sentence_length / 2.5)  

        return float(max(0, min(10, depth_score)))

    """
    Calculates the keyword density score of the essay based on the frequency of topic-specific keywords.
    Tokenize the essay text into words.
    Count the number of occurrences of topic keywords in the essay text.
    Calculate the density ratio as the number of keyword occurrences divided by the total number of words.
    The density score is scaled to a range of 0 to 10.
    Return the density score.
    """
    def calculate_keyword_density(self, essay_text, topic_keywords):
        
        words = nltk.word_tokenize(essay_text.lower())
        keyword_count = sum(1 for word in words if word in topic_keywords)
        density_ratio = keyword_count / len(words) if words else 0

        density_score = min(10, density_ratio * 200)  

        return float(max(0, min(10, density_score)))

    """
    Calculates all the scores for the essay, including originality, coherence, topic relevance, depth of analysis, and keyword density.
    Convert topic keywords to lowercase.
    Calculate each score using the respective methods.
    Return a dictionary containing all the scores.
    """
    def calculate_all_scores(self, essay_text, topic_keywords):
        
        topic_keywords = [keyword.lower() for keyword in (topic_keywords or [])]
        
        scores = {
            "originality_score": self.calculate_originality(essay_text),
            "coherence_score": self.calculate_coherence(essay_text),
            "topic_relevance_score": self.calculate_topic_relevance(essay_text, topic_keywords),
            "depth_of_analysis_score": self.calculate_depth_of_analysis(essay_text),
            "keyword_density_score": self.calculate_keyword_density(essay_text, topic_keywords)
        }
        return scores

    """
    Compares the user's feedback scores with the class average scores and generates a radar chart and HTML feedback.
    Define the categories for comparison.
    Calculate the class average scores for each category.
    Generate a radar chart comparing the user's scores with the class averages.
    Generate HTML feedback comparing the user's scores with the class averages.
    Return a dictionary containing the radar chart image path and the HTML feedback.
    """
    def compare_user_with_class(self, assignment_feedback, user_feedback):
        
        categories = [
            "originality_score", 
            "coherence_score", 
            "topic_relevance_score", 
            "depth_of_analysis_score", 
            "keyword_density_score"
        ]
        
        class_averages = {
            category: mean(feedback[category] for feedback in assignment_feedback) 
            for category in categories
        }
        
        user_scores = [user_feedback[category] for category in categories]
        avg_scores = [class_averages[category] for category in categories]
        
        radar_chart_img = self.generate_radar_chart(user_scores, avg_scores, categories)

        html_feedback = self.generate_html_feedback(user_scores, avg_scores, categories)

        return {"radar_chart_img": radar_chart_img, "inter_essay_feedback": html_feedback}

    """
    Generates a radar chart comparing the user's scores with the class average scores.
    Set up the radar chart with the user's scores and the class average scores.
    Plot the radar chart and save it as an image file.
    Save the radar chart image using the MediaService.
    Return the path to the saved radar chart image.
    """
    def generate_radar_chart(self, user_scores, avg_scores, categories): 
        num_vars = len(categories)
        
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        user_scores += user_scores[:1]  
        avg_scores += avg_scores[:1]    
        angles += angles[:1]           

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.plot(angles, avg_scores, color='red', linewidth=2, linestyle='solid', label='Class Average')
        ax.fill(angles, avg_scores, color='red', alpha=0.25)

        ax.plot(angles, user_scores, color='blue', linewidth=2, linestyle='solid', label='Student')
        ax.fill(angles, user_scores, color='blue', alpha=0.25)

        ax.set_yticks(np.arange(0, 11, 2))  
        ax.set_ylim(0, 10)

        plt.xticks(angles[:-1], categories, color='black', size=12)

        plt.title("Student vs Class Average Performance", size=15, pad=20)

        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        output_dir = "static/generated_result/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = str(int(time.time()))
        radar_chart_path = os.path.join(output_dir, f"radar_chart_{timestamp}.png")
        plt.savefig(radar_chart_path, format="png", bbox_inches="tight")
        plt.close(fig)

        self.media_service.saveMedia(
            {
                "file_path" : f"/{radar_chart_path}",
                "file_type" : "image",
                "uploaded_by" : None
            }
        )

        return f"/{radar_chart_path}"

    """
    Generates HTML feedback comparing the user's scores with the class average scores.
    Generate HTML feedback comparing the user's scores with the class averages.
    Provide suggestions for improvement based on the comparison.
    Return the HTML feedback as a string.
    """
    def generate_html_feedback(self, user_scores, avg_scores, categories):
        feedback_html = "<h2>User Feedback Comparison</h2><p>Below is a comparison of your scores against the class averages, with suggestions for each area:</p>"
        feedback_html += "<ul>"

        for i, category in enumerate(categories):
            user_score = user_scores[i]
            avg_score = avg_scores[i]
            feedback_html += f"<li><strong>{category.replace('_', ' ').capitalize()}:</strong> "

            if user_score > avg_score:
                feedback_html += f"Your score of {user_score} exceeds the class average of {avg_score:.2f}, indicating a strong performance in this area. "
            elif user_score < avg_score:
                feedback_html += f"Your score of {user_score} is below the class average of {avg_score:.2f}. Focusing on this area might help you improve. "
            else:
                feedback_html += f"Your score of {user_score} matches the class average, showing consistent performance with peers. "

            if category == "originality_score":
                if user_score <= 5:
                    feedback_html += "Incorporating unique perspectives or varied vocabulary might improve originality. Avoiding repetitive phrases might also help."
                elif 6 <= user_score <= 8:
                    feedback_html += "Good effort! Adding more distinct viewpoints or diverse vocabulary might further enhance originality."
                else:
                    feedback_html += "Excellent originality! Continuing to explore creative expressions might maintain this strength."

            elif category == "coherence_score":
                if user_score <= 5:
                    feedback_html += "Improving the flow between sentences might enhance coherence. Transitional phrases and clarity might help with readability."
                elif 6 <= user_score <= 8:
                    feedback_html += "Your essay is fairly coherent. Refining transitions and logical flow might bring coherence to an even higher level."
                else:
                    feedback_html += "Your essay is very coherent! Maintaining this flow and logic might help sustain reader engagement."

            elif category == "topic_relevance_score":
                if user_score <= 5:
                    feedback_html += "Focusing more directly on the main topic might improve relevance. Avoiding off-topic details might also help."
                elif 6 <= user_score <= 8:
                    feedback_html += "Good job staying relevant! Ensuring that each section directly supports the topic might further enhance relevance."
                else:
                    feedback_html += "Great relevance! Continuing to focus closely on the topic might keep arguments clear and compelling."

            elif category == "depth_of_analysis_score":
                if user_score <= 5:
                    feedback_html += "Exploring ideas in more depth might strengthen your analysis. Providing examples or explanations might improve support for your argument."
                elif 6 <= user_score <= 8:
                    feedback_html += "Your analysis is good but might be deeper. Adding additional details or evidence might further reinforce your points."
                else:
                    feedback_html += "Impressive depth! Continuing to include insightful analysis might sustain this strong performance."

            elif category == "keyword_density_score":
                if user_score <= 5:
                    feedback_html += "Incorporating more topic-specific keywords might help emphasize key themes. Avoiding overly generic language might also improve clarity."
                elif 6 <= user_score <= 8:
                    feedback_html += "Solid keyword usage! Ensuring essential terms are present without overloading might further enhance clarity."
                else:
                    feedback_html += "Great keyword density! Maintaining balanced keyword usage might help keep the essay focused and readable."

            feedback_html += "</li>"

        feedback_html += "</ul><p>The radar chart visually represents your performance relative to your classmates. A score closer to the edge indicates better performance, with a scale of 0 (worst) to 10 (best).</p>"
        return feedback_html

        

