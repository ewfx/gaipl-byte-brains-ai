import openai
import os
from typing import List, Dict, Any, Optional
from config.config import Config
import streamlit as st
import json
from datetime import datetime
import logging

class OpenAIService:
    def __init__(self):
        """Initialize OpenAI service with API key."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.AsyncOpenAI(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)
        self.model = Config.OPENAI_MODEL
        self.system_prompt = """You are an AI assistant for IT support. 
        You help with troubleshooting, incident management, and technical guidance. 
        Provide clear, concise responses and step-by-step solutions when applicable."""

    async def get_completion(self, prompt: str, model: str = "gpt-3.5-turbo", system_prompt: str = None) -> str:
        """
        Get completion from OpenAI API
        Args:
            prompt: The prompt to send to OpenAI
            model: The model to use (default: gpt-3.5-turbo)
            system_prompt: Optional system prompt to override default
        Returns:
            The completion text
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt or self.system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error getting OpenAI completion: {str(e)}")
            return f"Error: {str(e)}"

    async def get_embeddings(self, text: str) -> List[float]:
        """
        Get embeddings for text using OpenAI API
        Args:
            text: Text to get embeddings for
        Returns:
            List[float]: Text embeddings
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error getting embeddings: {str(e)}")

    async def analyze_text(self, text: str, analysis_type: str = "general") -> Dict[str, Any]:
        """
        Analyze text using OpenAI
        Args:
            text: The text to analyze
            analysis_type: Type of analysis to perform
        Returns:
            Dictionary containing analysis results
        """
        try:
            prompt = f"""
            Analyze the following text for {analysis_type}:
            
            {text}
            
            Provide your analysis in JSON format with appropriate fields based on the analysis type.
            """
            
            response = await self.get_completion(prompt)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "error": "Failed to parse analysis response",
                    "raw_response": response,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Error analyzing text: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text using OpenAI
        Args:
            text: Text to analyze
        Returns:
            Dict containing sentiment analysis
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Analyze the sentiment and respond with only 'positive', 'negative', or 'neutral'."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3
            )
            return {
                "text": text,
                "sentiment": response.choices[0].message.content.strip().lower(),
                "confidence": 0.8  # Placeholder confidence score
            }
        except Exception as e:
            return {
                "text": text,
                "sentiment": "unknown",
                "error": str(e)
            }

    async def summarize_text(self, text: str, max_length: int = 100) -> str:
        """
        Summarize text using OpenAI
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
        Returns:
            str: Summarized text
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"Summarize the following text in no more than {max_length} characters."},
                    {"role": "user", "content": text}
                ],
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error summarizing text: {str(e)}"

    async def categorize_text(self, text: str, categories: List[str]) -> str:
        """
        Categorize text into predefined categories
        Args:
            text: Text to categorize
            categories: List of possible categories
        Returns:
            str: Best matching category
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"Categorize the text into one of these categories: {categories}"},
                    {"role": "user", "content": text}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error categorizing text: {str(e)}"

    async def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        Args:
            text: Text to analyze
        Returns:
            Dict containing extracted entities
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """Extract and categorize entities into these categories:
                        - People
                        - Organizations
                        - Technical Terms
                        - Error Codes
                        Respond in JSON format."""},
                    {"role": "user", "content": text}
                ],
                temperature=0.3
            )
            return {
                "text": text,
                "entities": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "text": text,
                "error": str(e)
            }

    def render_validation_form(self):
        with st.form("validation_form"):
            input_value = st.text_input("Required Field")
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                if not input_value:
                    st.error("Please fill in all required fields")
                else:
                    st.success("Form submitted successfully!")

    def render_form_1(self):
        with st.form("form_1"):
            submitted_1 = st.form_submit_button("Submit 1")

    def render_form_2(self):
        with st.form("form_2"):
            submitted_2 = st.form_submit_button("Submit 2")

    def render_form_submission(self):
        if submitted:
            # Handle form submission outside the form
            st.success("Form submitted!")

    def render_form_with_unique_id(self):
        with st.form("unique_form_id"):
            # Form inputs here
            submitted = st.form_submit_button("Submit")

    def render_form_with_unique_id_2(self):
        with st.form("unique_form_id_2"):
            # Form inputs here
            submitted = st.form_submit_button("Submit") 