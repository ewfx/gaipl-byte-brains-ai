import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass

# Get user credentials from environment variables
USERS = {
    os.getenv("ADMIN_USERNAME", "admin"): {
        "password": os.getenv("ADMIN_PASSWORD", "admin123"),
        "role": "admin",
        "name": "Admin User"
    },
    os.getenv("SUPPORT_USERNAME", "support"): {
        "password": os.getenv("SUPPORT_PASSWORD", "support123"),
        "role": "support",
        "name": "Support User"
    },
    os.getenv("VIEWER_USERNAME", "viewer"): {
        "password": os.getenv("VIEWER_PASSWORD", "viewer123"),
        "role": "viewer",
        "name": "Viewer User"
    }
}

def check_authentication() -> bool:
    """
    Check if user is authenticated
    Returns:
        bool: True if authenticated, False otherwise
    """
    # Initialize session state for authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.login_time = None

    return st.session_state.authenticated

def show_login_form():
    """Show login form in sidebar"""
    st.sidebar.markdown("### Login")
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            try:
                authenticate_user(username, password)
                st.success("Login successful!")
                st.rerun()
            except AuthenticationError as e:
                st.error(str(e))
                logout_user()

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate user credentials and set session state
    Args:
        username: Username
        password: Password
    Returns:
        Dict containing user information if authenticated
    Raises:
        AuthenticationError if authentication fails
    """
    if not username or not password:
        raise AuthenticationError("Please enter both username and password")

    user = USERS.get(username)
    if not user:
        raise AuthenticationError("Invalid username")

    if user["password"] != password:  # In production, use proper password hashing
        raise AuthenticationError("Invalid password")

    # Set session state
    st.session_state.authenticated = True
    st.session_state.user = username
    st.session_state.role = user["role"]
    st.session_state.login_time = datetime.now()

    return {
        "name": user["name"],
        "role": user["role"]
    }

def logout_user():
    """Clear authentication session state"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.login_time = None

def check_role_permission(required_role: str) -> bool:
    """
    Check if current user has required role
    Args:
        required_role: Required role for access
    Returns:
        bool: True if user has required role, False otherwise
    """
    if not st.session_state.authenticated:
        return False

    role_hierarchy = {
        "admin": 3,
        "support": 2,
        "viewer": 1
    }

    return role_hierarchy.get(st.session_state.role, 0) >= role_hierarchy.get(required_role, 0)

def get_current_user() -> Optional[Dict]:
    """
    Get current user information
    Returns:
        Dict containing user information if authenticated, None otherwise
    """
    if not st.session_state.authenticated:
        return None

    return {
        "name": USERS[st.session_state.user]["name"],
        "role": st.session_state.role,
        "login_time": st.session_state.login_time
    }

def render_user_info():
    """Render user information in sidebar"""
    if st.session_state.authenticated:
        with st.sidebar:
            st.markdown("---")
            st.subheader("User Information")
            user_info = get_current_user()
            if user_info:
                st.write(f"Name: {user_info['name']}")
                st.write(f"Role: {user_info['role']}")
                if user_info.get('login_time'):
                    st.write(f"Login Time: {user_info['login_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            if st.button("Logout", key="auth_logout_button"):
                logout_user()
                st.rerun() 