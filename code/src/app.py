import streamlit as st
from config.config import Config
from components.sidebar import render_sidebar
from components.chat_interface import ChatInterface
from components.telemetry_dashboard import TelemetryDashboard
from components.automation_panel import AutomationPanel
from components.knowledge_base import KnowledgeBase
from components.log_analyzer import LogAnalyzer
from components.ticket_analyzer import TicketAnalyzer
from components.recommendation_dashboard import RecommendationDashboard
from utils.session_state import initialize_session_state
from utils.auth import check_authentication, check_role_permission, show_login_form
from utils.openai_service import OpenAIService
from services.agent_service import AgentService
from services.recommendation_service import RecommendationService

def main():
    try:
        # Validate configuration
        Config.validate()
        
        st.set_page_config(
            page_title="ByteBrains Agentic AI Platform",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Initialize session state
        initialize_session_state()

        # Check authentication before proceeding
        if not check_authentication():
            show_login_form()
            return

        # Initialize services
        agent_service = AgentService()
        openai_service = OpenAIService()
        recommendation_service = RecommendationService()

        # Store services in session state for access across components
        if 'agent_service' not in st.session_state:
            st.session_state.agent_service = agent_service

        # Main application layout
        st.title("ByteBrains Integrated Agentic AI Platform Environment")

        # Render sidebar and get current page
        current_page = render_sidebar()

        # Initialize components
        automation_panel = AutomationPanel()
        log_analyzer = LogAnalyzer()
        ticket_analyzer = TicketAnalyzer()
        recommendation_dashboard = RecommendationDashboard(recommendation_service)

        # Main content area based on selected page
        if current_page == "Dashboard":
            if check_role_permission("viewer"):
                TelemetryDashboard().render()
            else:
                st.error("Insufficient permissions")
                
        elif current_page == "Chat Support":
            if check_role_permission("support"):
                ChatInterface().render()
            else:
                st.error("Insufficient permissions")
                
        elif current_page == "Automation":
            if check_role_permission("support"):
                automation_panel.render()
            else:
                st.error("Insufficient permissions")
                
        elif current_page == "Knowledge Base":
            if check_role_permission("viewer"):
                KnowledgeBase().render()
            else:
                st.error("Insufficient permissions")
                
        elif current_page == "Log Analysis":
            if check_role_permission("viewer"):
                log_analyzer.render()
            else:
                st.error("Insufficient permissions")
                
        elif current_page == "Ticket Analysis":
            if check_role_permission("viewer"):
                ticket_analyzer.render()
            else:
                st.error("Insufficient permissions")

        elif current_page == "Recommendations Engine":
            recommendation_dashboard.render()

    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.info("Please set up your .env file with the required API keys.")
        return

if __name__ == "__main__":
    main() 