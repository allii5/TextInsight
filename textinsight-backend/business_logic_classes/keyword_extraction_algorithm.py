import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from concurrent.futures import ThreadPoolExecutor, as_completed
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
wn.ensure_loaded() 
from nltk.stem import WordNetLemmatizer
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
from matplotlib_venn import venn3
from matplotlib import pyplot as plt
import os
import time
from media.service import MediaService

class Algorithm:

    """
    Initializes the Algorithm class with necessary NLTK downloads and services.
    Download required NLTK datasets.
    Initialize stop words, lemmatizer, and media service.
    """
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        self.stop_words = set(stopwords.words('english'))  
        self.lemmatizer = WordNetLemmatizer()
        self.media_service = MediaService()  

    """
    Preprocesses the input text by converting it to lowercase, removing non-alphanumeric characters,
    tokenizing, removing stop words, and lemmatizing the tokens.
    """
    def _preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in filtered_tokens]
        return lemmatized_tokens

    """
    Extracts keywords from the text using the TextRank algorithm.
    Tokenizes the text into sentences and preprocesses each sentence.
    Builds a graph where nodes are words and edges represent co-occurrence within sentences.
    Calculates PageRank scores for each word and returns the top N keywords.
    """
    def _textrank_keywords(self, text, n=10):
        sentences = sent_tokenize(text)
        tokenized_sentences = [self._preprocess_text(sentence) for sentence in sentences]
        graph = nx.Graph()
        for sentence in tokenized_sentences:
            graph.add_nodes_from(sentence)
            for word1 in sentence:
                for word2 in sentence:
                    if word1 != word2:
                        graph.add_edge(word1, word2)
        scores = nx.pagerank(graph)
        keywords = sorted(scores, key=scores.get, reverse=True)[:n]
        return keywords

    """
    Extracts keywords from the text using the Eigenvector Centrality algorithm.
    Preprocesses the text to get tokens and builds a graph where nodes are words.
    Calculates Eigenvector Centrality scores for each word and returns the top N keywords.
    """
    def _eigenvector_keywords(self, text, n=10):
        tokens = self._preprocess_text(text)
        graph = nx.Graph()
        graph.add_nodes_from(tokens)
        scores = nx.eigenvector_centrality(graph)
        keywords = sorted(scores, key=scores.get, reverse=True)[:n]
        return keywords

    """
    Extracts keywords from the text using the Betweenness Centrality algorithm.
    Preprocesses the text to get tokens and builds a graph where nodes are words.
    Calculates Betweenness Centrality scores for each word and returns the top N keywords.
    """
    def _betweenness_keywords(self, text, n=10):
        tokens = self._preprocess_text(text)
        graph = nx.Graph()
        graph.add_nodes_from(tokens)
        scores = nx.betweenness_centrality(graph)
        keywords = sorted(scores, key=scores.get, reverse=True)[:n]
        return keywords

    """
    Combines the scores from TextRank, Eigenvector Centrality, and Betweenness Centrality algorithms.
    Calculates a combined score for each keyword and returns the top N keywords.
    """
    def _combine_scores(self, text, n=10):
        textrank_scores = Counter(self._textrank_keywords(text, n))
        eigenvector_scores = Counter(self._eigenvector_keywords(text, n))
        betweenness_scores = Counter(self._betweenness_keywords(text, n))
        combined_scores = {}
        for keyword in set(textrank_scores.keys()) | set(eigenvector_scores.keys()) | set(betweenness_scores.keys()):
            combined_scores[keyword] = (
                textrank_scores.get(keyword, 0) +
                eigenvector_scores.get(keyword, 0) +
                betweenness_scores.get(keyword, 0)
            )
        keywords = sorted(combined_scores, key=combined_scores.get, reverse=True)[:n]
        return keywords

    """
    Builds and visualizes a graph of keywords from the text.
    Tokenizes the text into sentences and preprocesses each sentence.
    Builds a graph where nodes are keywords and edges represent co-occurrence within sentences.
    Uses PyVis to visualize the graph and saves the HTML file.
    """
    def _build_and_visualize_graph(self, text, keywords, output_path):
        sentences = sent_tokenize(text)
        tokenized_sentences = [self._preprocess_text(sentence) for sentence in sentences]
        graph = nx.Graph()
        for keyword in keywords:
            graph.add_node(keyword)
        for sentence in tokenized_sentences:
            for word1 in sentence:
                for word2 in sentence:
                    if word1 in keywords and word2 in keywords and word1 != word2:
                        if graph.has_edge(word1, word2):
                            graph[word1][word2]['weight'] += 1
                        else:
                            graph.add_edge(word1, word2, weight=1)

        net = Network(notebook=True)
        for node in graph.nodes():
            net.add_node(node, label=node)
        for edge in graph.edges(data=True):
            net.add_edge(edge[0], edge[1], value=edge[2]['weight'])
        
        self.media_service.saveMedia(
            {
                "file_path" : f"/{output_path}",
                "file_type" : "html",
                "uploaded_by" : None
            }
        )

        net.show(output_path)

    """
    Creates a Venn diagram using Matplotlib to visualize the overlap of keywords between different sections.
    Saves the Venn diagram as an image file.
    """
    def _create_venn_diagram_by_matplotlib(self, set1, set2, set3=None, output_path="venn_diagram.png"):
        plt.figure(figsize=(8, 8))
        
        venn = venn3([set1, set2, set3], ('Introduction', 'Middle', 'Conclusion'))

        plt.savefig(output_path)
        plt.close()

        self.media_service.saveMedia(
            {
                "file_path" : f"/{output_path}",
                "file_type" : "image",
                "uploaded_by" : None
            }
        )
    
    """
    Creates a word cloud visualization of the keywords.
    Generates the word cloud image and saves it as a file.
    """
    def _create_wordcloud(self, keywords, wordcloud_path):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(keywords)
        wordcloud.to_file(wordcloud_path)

        self.media_service.saveMedia(
            {
                "file_path" : f"/{wordcloud_path}",
                "file_type" : "image",
                "uploaded_by" : None
            }
        )

    """
    Extracts keywords from the introduction, middle, and conclusion sections in parallel.
    Returns the keywords for each section.
    """
    def _extract_keywords_parallel(self, introduction, middle, conclusion):
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._combine_scores, introduction),
                executor.submit(self._combine_scores, middle),
                executor.submit(self._combine_scores, conclusion),
            ]
            for future in as_completed(futures):
                results.append(future.result())

        return results[0], results[1], results[2]

    """
    Generates visualizations (graph, Venn diagram, word cloud) in parallel.
    Returns the paths to the generated visualizations.
    """
    def _generate_visuals_parallel(self, combine_text, keywords, output_dir, timestamp, introduction_keywords, middle_keywords, conclusion_keywords):
        with ThreadPoolExecutor() as executor:
            graph_path = os.path.join(output_dir, f"keywords_graph_{timestamp}.html")
            venn_path = os.path.join(output_dir, f"venn_diagram_{timestamp}.png")
            wordcloud_path = os.path.join(output_dir, f"wordcloud_{timestamp}.png")

            graph_future = executor.submit(self._build_and_visualize_graph, combine_text, keywords, graph_path)
            venn_future = executor.submit(self._create_venn_diagram_by_matplotlib, set(introduction_keywords), set(middle_keywords), set(conclusion_keywords), venn_path)
            wordcloud_future = executor.submit(self._create_wordcloud, ' '.join(keywords), wordcloud_path)

            return graph_path, venn_path, wordcloud_path

    """
    Performs all the keyword extraction and visualization tasks.
    Extracts keywords from the introduction, middle, and conclusion sections.
    Generates visualizations (graph, Venn diagram, word cloud) and returns the paths and keywords.
    """
    def do_all_working(self, introduction, middle, conclusion):
        intro_keywords, middle_keywords, conclusion_keywords = self._extract_keywords_parallel(introduction, middle, conclusion)

        keywords = intro_keywords + middle_keywords + conclusion_keywords
        combine_text = introduction + ' ' + middle + ' ' + conclusion


        output_dir = "static/generated_result/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = str(int(time.time()))

        graph_path, venn_path, wordcloud_path = self._generate_visuals_parallel(combine_text, keywords, output_dir, timestamp, intro_keywords, middle_keywords, conclusion_keywords)

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(lambda: list(set(intro_keywords) & set(middle_keywords))),
                executor.submit(lambda: list(set(intro_keywords) & set(conclusion_keywords))),
                executor.submit(lambda: list(set(middle_keywords) & set(conclusion_keywords))),
                executor.submit(lambda: list(set(intro_keywords) & set(middle_keywords) & set(conclusion_keywords)))
            ]
            common_intro_mid, common_intro_conclusion, common_mid_conclusion, common_intro_mid_conclusion = [f.result() for f in futures]

        return {
            "keyword_graph_html": f"/{graph_path}",
            "venn_diagram_image": f"/{venn_path}",
            "wordcloud_image": f"/{wordcloud_path}",
            "keywords" : keywords,
            "intro_keywords": intro_keywords,
            "middle_keywords": middle_keywords,
            "conclusion_keywords": conclusion_keywords,
            "intro_mid_keywords": common_intro_mid,
            "intro_conclusion_keywords": common_intro_conclusion,
            "mid_conclusion_keywords": common_mid_conclusion,
            "intro_mid_conclusion_keywords": common_intro_mid_conclusion
        }
