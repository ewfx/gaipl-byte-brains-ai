import streamlit as st
from utils.session_state import get_current_incident, clear_current_incident, update_current_incident

def render_sidebar() -> str:
    """
    Render the sidebar navigation and return the selected page
    Returns:
        str: The currently selected page
    """
    with st.sidebar:
        st.title("Navigation")
        
        # Navigation options
        options = [
            "Dashboard",
            "Chat Support",
            "Automation",
            "Knowledge Base",
            "Log Analysis",
            "Ticket Analysis",
            "Recommendations Engine"
        ]
        
        # Get current page from session state or default to Dashboard
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"
            
        # Create radio buttons for navigation
        selected_page = st.radio(
            "Select a page",
            options,
            index=options.index(st.session_state.current_page),
            key="sidebar_navigation"
        )
        
        # Update current page in session state
        st.session_state.current_page = selected_page
        
        # Show current context if available
        current_incident = get_current_incident()
        if current_incident:
            st.sidebar.markdown("---")
            st.sidebar.subheader("Current Context")
            st.sidebar.info(
                f"Incident: {current_incident['id']} - {current_incident['title']}\n"
                f"Priority: {current_incident['priority']}"
            )
            if st.sidebar.button("Clear Incident", key="clear_incident_button"):
                clear_current_incident()
                st.rerun()
        
        # Add user info section
        st.sidebar.markdown("---")
        st.sidebar.subheader("User Info")
        if "user" in st.session_state:
            st.sidebar.text(f"User: {st.session_state.user}")
            if st.sidebar.button("Logout", key="sidebar_logout_button"):
                st.session_state.clear()
                st.rerun()

    return selected_page 