import streamlit as st
from datetime import datetime
from typing import Dict, Any

def initialize_session_state():
    """
    Initialize the session state with default values
    This function sets up all the necessary session state variables
    """
    # User and Authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "role" not in st.session_state:
        st.session_state.role = None

    if "login_time" not in st.session_state:
        st.session_state.login_time = None

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Current Context
    if "current_incident" not in st.session_state:
        st.session_state.current_incident = None

    if "current_ci" not in st.session_state:
        st.session_state.current_ci = None

    # Telemetry Settings
    if "telemetry_refresh_rate" not in st.session_state:
        st.session_state.telemetry_refresh_rate = 60  # seconds

    if "last_telemetry_update" not in st.session_state:
        st.session_state.last_telemetry_update = None

    # Knowledge Base
    if "recent_searches" not in st.session_state:
        st.session_state.recent_searches = []

    if "kb_favorites" not in st.session_state:
        st.session_state.kb_favorites = []

    # Automation History
    if "automation_history" not in st.session_state:
        st.session_state.automation_history = []

def get_session_info() -> Dict[str, Any]:
    """
    Get current session information
    Returns:
        Dict containing session information
    """
    return {
        "authenticated": st.session_state.authenticated,
        "user": st.session_state.user,
        "login_time": st.session_state.login_time,
        "current_incident": st.session_state.current_incident,
        "current_ci": st.session_state.current_ci
    }

def update_session_context(context_type: str, value: Any):
    """
    Update session context
    Args:
        context_type: Type of context to update (e.g., 'incident', 'ci')
        value: New value for the context
    """
    if context_type == "incident":
        st.session_state.current_incident = value
    elif context_type == "ci":
        st.session_state.current_ci = value
    elif context_type == "user":
        st.session_state.user = value
        st.session_state.authenticated = bool(value)
        st.session_state.login_time = datetime.now() if value else None

def clear_session():
    """Clear all session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()

def add_to_chat_history(message: Dict[str, Any]):
    """
    Add a message to chat history
    Args:
        message: Message dictionary containing role and content
    """
    if "messages" in st.session_state:
        st.session_state.messages.append(message)

def add_to_automation_history(action: Dict[str, Any]):
    """
    Add an automation action to history
    Args:
        action: Action dictionary containing details of the automation
    """
    if "automation_history" in st.session_state:
        st.session_state.automation_history.append({
            **action,
            "timestamp": datetime.now()
        })

def add_to_recent_searches(search_query: str):
    """
    Add a search query to recent searches
    Args:
        search_query: Search query string
    """
    if "recent_searches" in st.session_state:
        # Add to start of list and maintain unique entries
        st.session_state.recent_searches = (
            [search_query] + 
            [s for s in st.session_state.recent_searches if s != search_query]
        )[:10]  # Keep only last 10 searches

def toggle_kb_favorite(item_id: str):
    """
    Toggle an item in KB favorites
    Args:
        item_id: ID of the knowledge base item
    """
    if "kb_favorites" in st.session_state:
        if item_id in st.session_state.kb_favorites:
            st.session_state.kb_favorites.remove(item_id)
        else:
            st.session_state.kb_favorites.append(item_id)

def update_current_incident(incident_data: Dict[str, Any] = None):
    """
    Update the current incident in session state
    Args:
        incident_data: Dictionary containing incident information
    """
    st.session_state.current_incident = incident_data

def get_current_incident() -> Dict[str, Any]:
    """
    Get the current incident from session state
    Returns:
        Dict containing current incident information or None
    """
    return st.session_state.current_incident

def clear_current_incident():
    """Clear the current incident from session state"""
    st.session_state.current_incident = None 