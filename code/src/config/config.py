import os
from dotenv import load_dotenv
import streamlit as st
# Load environment variables from .env file
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    # OPENAI_API_KEY = st.secrets["OPEN_AI_KEY"]
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Application Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Vector Store Configuration
    VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH', './data/vector_store')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        
        if not Config.OPENAI_MODEL:
            raise ValueError("OPENAI_MODEL is not set in environment variables")

    @staticmethod
    def get_openai_config() -> dict:
        """Get OpenAI configuration"""
        return {
            "api_key": Config.OPENAI_API_KEY,
            "model": Config.OPENAI_MODEL
        } 