import spacy
from sentence_transformers import SentenceTransformer, util
from concurrent.futures import ThreadPoolExecutor

class EssayFeedback:
    # Initializes the EssayFeedback class with SpaCy and SentenceTransformer models
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    """
    Evaluates the diversity of sentence lengths in the document
    Identify long sentences (more than 25 words)
    Provide feedback on sentence length and suggest breaking down long sentences
    Return feedback on sentence diversity
    """
    def evaluate_sentence_diversity(self, doc):
        long_sentences = [sent for sent in doc.sents if len(sent.text.split()) > 25]
        if long_sentences:
            feedback = "Some sentences are too long (more than 25 words):<br>"
            feedback += "".join(f"  - {sent.text}<br>" for sent in long_sentences)
            feedback += "Suggestion: Try to break down long sentences into shorter, clearer ones. Use a mix of short and long sentences for better readability.<br>"
        else:
            feedback = "Sentence length is varied and appropriate.<br>"
        return feedback

    """
    Evaluates the coherence between consecutive sentences
    Calculate the cosine similarity between consecutive sentence embeddings
    Provide feedback on coherence issues between sentences
    Return feedback on sentence coherence
    """
    def evaluate_coherence(self, sentences, embeddings):
        feedback = ""
        for i in range(1, len(sentences)):
            similarity = util.pytorch_cos_sim(embeddings[i-1], embeddings[i]).item()
            if similarity < 0.3:
                feedback += f"Coherence issue between sentences: '{sentences[i-1]}' and '{sentences[i]}'.<br>"
        return feedback if feedback else "Sentences are coherent and logically connected.<br>"

    """
    Evaluates the effectiveness of the conclusion in summarizing the main points
    Combine the introduction and middle sections
    Encode the combined text and the conclusion to generate embeddings
    Calculate the cosine similarity between the combined text and the conclusion
    Provide feedback on the effectiveness of the conclusion
    Return feedback on the conclusion
    """
    def evaluate_conclusion(self, intro, middle, conclusion):
        intro_middle_text = intro + " " + middle
        embeddings = self.model.encode([intro_middle_text, conclusion], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

        if similarity < 0.5:
            feedback = "The conclusion does not effectively summarize the main points.<br>"
            feedback += "Suggestion: Make sure the conclusion brings together all the main points discussed in the essay and restates the thesis in a new way.<br>"
        else:
            feedback = "The conclusion effectively summarizes the main points.<br>"
        
        return feedback

    """
    Evaluates the coherence between different sections of the essay
    Encode the sections to generate embeddings
    Calculate the cosine similarity between consecutive section embeddings
    Provide feedback on coherence issues between sections
    Return feedback on section coherence
    """
    def evaluate_section_coherence(self, sections, section_names):
        embeddings = self.model.encode(sections, convert_to_tensor=True)
        feedback = ""
        
        for i in range(1, len(sections)):
            similarity = util.pytorch_cos_sim(embeddings[i-1], embeddings[i]).item()
            if similarity < 0.5:
                feedback += f"Coherence issue between {section_names[i-1]} and {section_names[i]}.<br>"
        
        return feedback if feedback else "Sections are coherent and logically connected.<br>"

    """
    Generates feedback for a specific section of the essay
    Process the section using SpaCy
    Evaluate sentence diversity and coherence within the section
    Return feedback for the section
    """
    def generate_section_feedback(self, section, section_name):
        doc = self.nlp(section)
        feedback = f"<p><strong>Feedback for {section_name}:</strong></p>"
        feedback += self.evaluate_sentence_diversity(doc)

        sentences = [sent.text for sent in doc.sents]
        embeddings = self.model.encode(sentences, convert_to_tensor=True)
        feedback += self.evaluate_coherence(sentences, embeddings)
        feedback += "<br>"
        
        return feedback

    """
    Generates overall feedback for the essay
    Define the sections and their names
    Use ThreadPoolExecutor to concurrently generate section feedbacks, conclusion feedback, and section coherence feedback
    Combine all feedbacks into a single string
    Return the overall feedback for the essay
    """
    def generate_overall_feedback(self, intro, middle, conclusion):
        sections = [intro, middle, conclusion]
        section_names = ['Introduction', 'Middle', 'Conclusion']
        
        with ThreadPoolExecutor() as executor:
            section_feedbacks = list(executor.map(self.generate_section_feedback, sections, section_names))
            conclusion_feedback = executor.submit(self.evaluate_conclusion, intro, middle, conclusion)
            section_coherence_feedback = executor.submit(self.evaluate_section_coherence, sections, section_names)
        
        feedback = "".join(section_feedbacks)
        feedback += conclusion_feedback.result()
        feedback += section_coherence_feedback.result()
        
        return feedback
