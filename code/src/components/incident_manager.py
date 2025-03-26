import streamlit as st
import pandas as pd
from services.data_service import DataService

class IncidentManager:
    def __init__(self):
        self.data_service = DataService()

    def render(self):
        st.header("Incident Management")

        # Load incident data
        incidents_df = self.data_service.load_dataset("incidents")
        jira_df = self.data_service.load_dataset("jira")

        # Combine and display incident information
        self.display_active_incidents(incidents_df)
        self.display_related_issues(jira_df)

    def display_active_incidents(self, incidents_df: pd.DataFrame):
        st.subheader("Active Incidents")
        
        # Filter active incidents
        active = incidents_df[incidents_df['status'] == 'active']
        
        # Display in a table
        st.dataframe(
            active[['incident_id', 'priority', 'description', 'created_at']],
            use_container_width=True
        )

    def display_related_issues(self, jira_df: pd.DataFrame):
        st.subheader("Related JIRA Issues")
        
        # Get current incident (if any)
        if 'current_incident' in st.session_state:
            incident_id = st.session_state.current_incident
            
            # Find related issues
            related = self.find_related_issues(jira_df, incident_id)
            
            # Display related issues
            st.dataframe(related, use_container_width=True) 