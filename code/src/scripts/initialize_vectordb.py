import streamlit as st
from services.data_service import DataService

def initialize_vector_database():
    st.title("Vector Database Initialization")
    
    data_service = DataService()
    
    with st.spinner("Initializing vector database..."):
        try:
            data_service.initialize_vector_store()
            st.success("Vector database initialized successfully!")
            
            # Test searches
            test_query = "server high CPU usage"
            
            st.subheader("Test Search Results")
            
            st.write("Similar Incidents:")
            incidents = data_service.search_similar_incidents(test_query)
            st.json(incidents)
            
            st.write("Relevant KB Articles:")
            articles = data_service.search_kb_articles(test_query)
            st.json(articles)
            
        except Exception as e:
            st.error(f"Error initializing vector database: {str(e)}")

if __name__ == "__main__":
    initialize_vector_database() 