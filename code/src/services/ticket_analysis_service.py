import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import json
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')
    nltk.download('omw-1.4')  # Open Multilingual Wordnet
    nltk.download('averaged_perceptron_tagger')  # Required for lemmatization

class TicketAnalysisService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self._ticket_data = None
        
    def load_sample_data(self) -> pd.DataFrame:
        """
        Load ticket data from the dataset
        Returns:
            pd.DataFrame: Ticket data
        """
        if self._ticket_data is not None:
            return self._ticket_data
            
        try:
            # Try to load from the data directory
            data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'sample', 'jira_tickets.json')
            with open(data_path, 'r') as f:
                tickets = json.load(f)
                
            # Convert to DataFrame
            df = pd.DataFrame(tickets)
            
            # Ensure required columns exist
            required_columns = ['ticket_id', 'title', 'description', 'created_date', 'status', 'priority', 'assignee', 'component']
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None
                    
            # Convert date strings to datetime
            if 'created_date' in df.columns:
                df['created_date'] = pd.to_datetime(df['created_date'])
                
            self._ticket_data = df
            return df
            
        except Exception as e:
            print(f"Error loading ticket data: {str(e)}")
            # Fallback to sample data if loading fails
            return self._generate_sample_data()
            
    def _generate_sample_data(self) -> pd.DataFrame:
        """Generate sample ticket data as fallback"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate random dates
        dates = pd.date_range(start='2023-01-01', end='2024-02-20', periods=n_samples)
        
        # Sample data
        data = {
            'ticket_id': [f'JIRA-{i:04d}' for i in range(n_samples)],
            'title': [f'Sample Ticket {i}' for i in range(n_samples)],
            'description': [f'This is a sample ticket description {i} with some technical details and issues.' for i in range(n_samples)],
            'created_date': dates,
            'status': np.random.choice(['Open', 'In Progress', 'Resolved', 'Closed'], n_samples),
            'priority': np.random.choice(['Critical', 'High', 'Medium', 'Low'], n_samples),
            'assignee': np.random.choice(['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Wilson'], n_samples),
            'component': np.random.choice(['Frontend', 'Backend', 'Database', 'Infrastructure'], n_samples),
            'resolution_time': np.random.randint(1, 30, n_samples),
            'severity': np.random.choice(['Critical', 'High', 'Medium', 'Low'], n_samples),
            'type': np.random.choice(['Bug', 'Feature', 'Task', 'Incident'], n_samples),
            'resolution_comment': [
                f'Issue resolved by implementing fix {i}. Root cause was identified and addressed.' 
                if np.random.random() > 0.5 else None 
                for i in range(n_samples)
            ],
            'server_details': [
                f'Server: server-{np.random.randint(1, 5)}\n'
                f'Environment: {np.random.choice(["Production", "Staging", "Development"])}\n'
                f'Region: {np.random.choice(["US-East", "US-West", "EU-Central", "Asia-Pacific"])}'
                if np.random.random() > 0.3 else None
                for i in range(n_samples)
            ]
        }
        
        df = pd.DataFrame(data)
        self._ticket_data = df
        return df
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for analysis
        Args:
            text: Input text
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        return ' '.join(tokens)
    
    def analyze_ticket_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze ticket trends
        Args:
            df: Ticket data
        Returns:
            Dict containing trend analysis results
        """
        # Time-based analysis
        df['created_date'] = pd.to_datetime(df['created_date'])
        df['month'] = df['created_date'].dt.to_period('M')
        
        # Monthly ticket counts
        monthly_counts = df.groupby('month').size().reset_index(name='count')
        
        # Priority distribution
        priority_dist = df['priority'].value_counts().to_dict()
        
        # Status distribution
        status_dist = df['status'].value_counts().to_dict()
        
        # Component distribution
        component_dist = df['component'].value_counts().to_dict()
        
        # Average resolution time by priority
        avg_resolution = df.groupby('priority')['resolution_time'].mean().to_dict()
        
        return {
            'monthly_counts': monthly_counts,
            'priority_distribution': priority_dist,
            'status_distribution': status_dist,
            'component_distribution': component_dist,
            'avg_resolution_time': avg_resolution
        }
    
    def analyze_ticket_content(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze ticket content using NLP
        Args:
            df: Ticket data
        Returns:
            Dict containing content analysis results
        """
        # Preprocess descriptions
        df['processed_description'] = df['description'].apply(self.preprocess_text)
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(df['processed_description'])
        
        # Perform clustering
        n_clusters = 5
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(tfidf_matrix)
        
        # Get top terms for each cluster
        feature_names = self.vectorizer.get_feature_names_out()
        cluster_terms = {}
        
        for i in range(n_clusters):
            cluster_docs = tfidf_matrix[clusters == i]
            if cluster_docs.shape[0] > 0:
                avg_tfidf = cluster_docs.mean(axis=0).A1
                top_indices = avg_tfidf.argsort()[-10:][::-1]
                top_terms = [feature_names[idx] for idx in top_indices]
                cluster_terms[f'Cluster {i+1}'] = top_terms
        
        return {
            'clusters': clusters.tolist(),
            'cluster_terms': cluster_terms
        }
    
    def generate_insights(self, df: pd.DataFrame) -> List[str]:
        """
        Generate insights from ticket data
        Args:
            df: Ticket data
        Returns:
            List of insights
        """
        insights = []
        
        # Priority insights
        critical_tickets = df[df['priority'] == 'Critical']
        if len(critical_tickets) > 0:
            insights.append(f"Found {len(critical_tickets)} critical tickets requiring immediate attention")
        
        # Resolution time insights
        avg_resolution = df['resolution_time'].mean()
        insights.append(f"Average ticket resolution time is {avg_resolution:.1f} days")
        
        # Component insights
        component_counts = df['component'].value_counts()
        most_affected = component_counts.index[0]
        insights.append(f"Most affected component is {most_affected} with {component_counts[0]} tickets")
        
        # Status insights
        open_tickets = df[df['status'] == 'Open']
        if len(open_tickets) > 0:
            insights.append(f"There are {len(open_tickets)} open tickets requiring attention")
        
        return insights 