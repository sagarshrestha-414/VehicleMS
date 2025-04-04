import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class VehicleChatbot:
    def __init__(self, intents_file):
        self.load_intents(intents_file)
        self.train_model()
    
    def load_intents(self, intents_file):
        with open(intents_file) as f:
            self.intents = json.load(f)
        
        self.patterns = []
        self.tags = []
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                self.patterns.append(pattern.lower())
                self.tags.append(intent['tag'])
    
    def train_model(self):
        self.vectorizer = TfidfVectorizer()
        self.pattern_vectors = self.vectorizer.fit_transform(self.patterns)
    
    def process_query(self, query):
        try:
            query = query.lower()
            query_vec = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vec, self.pattern_vectors)
            best_match_idx = np.argmax(similarities)
            
            for intent in self.intents['intents']:
                if self.patterns[best_match_idx] in intent['patterns']:
                    return np.random.choice(intent['responses'])
            
            return "I'm not sure about that vehicle question. Can you rephrase?"
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I'm having trouble understanding that. Could you try again?"