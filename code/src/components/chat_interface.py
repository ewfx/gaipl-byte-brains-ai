import streamlit as st
from services.data_service import DataService
from services.openai_service import OpenAIService
from services.agent_service import AgentService
from services.ticket_analysis_service import TicketAnalysisService
from services.log_service import LogService
import pandas as pd
from datetime import datetime

class ChatInterface:
    def __init__(self):
        self.data_service = DataService()
        self.openai_service = OpenAIService()
        self.agent_service = AgentService()
        self.ticket_service = TicketAnalysisService()
        self.log_service = LogService()

    def render(self):
        st.header("AI Support Assistant")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Load data for context
        incidents = self.data_service.get_incidents()
        kb_articles = self.data_service.get_kb_articles()
        tickets = self.ticket_service.load_sample_data()
        logs = self.log_service.get_logs(application="all", server="all")
        automation_tasks = self.agent_service.get_active_tasks()

        # Chat input
        if prompt := st.chat_input("How can I help you?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get relevant context from all sources
            context = self.get_relevant_context(prompt, {
                'incidents': incidents,
                'kb_articles': kb_articles,
                'tickets': tickets,
                'logs': logs,
                'automation_tasks': automation_tasks
            })

            # Get AI response
            response = self.openai_service.get_completion(prompt, context)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def get_relevant_context(self, query: str, data_sources: dict) -> dict:
        """Get relevant context from all data sources"""
        context = {}
        
        # Get relevant incidents
        if not data_sources['incidents'].empty:
            context['incidents'] = self.find_relevant_incidents(query, data_sources['incidents'])
        
        # Get relevant KB articles
        if not data_sources['kb_articles'].empty:
            context['kb_articles'] = self.find_relevant_articles(query, data_sources['kb_articles'])
        
        # Get relevant tickets and ticket statistics
        if not data_sources['tickets'].empty:
            context['tickets'] = self.find_relevant_tickets(query, data_sources['tickets'])
            context['ticket_stats'] = self.get_ticket_statistics(data_sources['tickets'])
        
        # Get relevant logs
        if data_sources['logs']:
            context['logs'] = self.find_relevant_logs(query, data_sources['logs'])
        
        # Get relevant automation tasks
        if data_sources['automation_tasks']:
            context['automation_tasks'] = self.find_relevant_tasks(query, data_sources['automation_tasks'])
        
        return context

    def find_relevant_incidents(self, query: str, incidents: pd.DataFrame) -> pd.DataFrame:
        """Find relevant incidents using semantic search"""
        return incidents[
            incidents['title'].str.contains(query, case=False) |
            incidents['description'].str.contains(query, case=False)
        ].head(3)

    def find_relevant_articles(self, query: str, articles: pd.DataFrame) -> pd.DataFrame:
        """Find relevant KB articles using semantic search"""
        return articles[
            articles['title'].str.contains(query, case=False) |
            articles['content'].str.contains(query, case=False)
        ].head(3)

    def find_relevant_tickets(self, query: str, tickets: pd.DataFrame) -> pd.DataFrame:
        """Find relevant tickets using semantic search"""
        # First, check if query contains a ticket ID
        ticket_id_match = None
        if 'JIRA-' in query.upper():
            try:
                # Extract ticket ID from query (e.g., "JIRA-0002" -> "JIRA-0002")
                ticket_id = query.upper().split('JIRA-')[1].split()[0]
                ticket_id = f"JIRA-{ticket_id}"
                ticket_id_match = tickets[tickets['ticket_id'] == ticket_id]
                if not ticket_id_match.empty:
                    return ticket_id_match
            except:
                pass

        # If no ticket ID match, search by title and description
        matching_tickets = tickets[
            tickets['title'].str.contains(query, case=False) |
            tickets['description'].str.contains(query, case=False)
        ]
        
        # If we have matching tickets, return up to 3 of them
        if not matching_tickets.empty:
            return matching_tickets.head(3)
        
        # If no matching tickets, try to match by status keywords
        status_keywords = {
            'open': ['open', 'new', 'pending'],
            'in progress': ['in progress', 'working', 'processing'],
            'resolved': ['resolved', 'fixed', 'completed'],
            'closed': ['closed', 'done', 'finished']
        }
        
        for status, keywords in status_keywords.items():
            if any(keyword in query.lower() for keyword in keywords):
                status_tickets = tickets[tickets['status'].str.lower() == status]
                if not status_tickets.empty:
                    return status_tickets.head(3)
        
        # If no status-specific tickets found, return 3 random tickets
        return tickets.sample(n=min(3, len(tickets)))

    def get_ticket_statistics(self, tickets: pd.DataFrame) -> dict:
        """Get accurate ticket statistics"""
        stats = {
            'total_tickets': len(tickets),
            'status_counts': tickets['status'].value_counts().to_dict(),
            'priority_counts': tickets['priority'].value_counts().to_dict(),
            'component_counts': tickets['component'].value_counts().to_dict()
        }
        return stats

    def find_relevant_logs(self, query: str, logs: list) -> list:
        """Find relevant logs using semantic search"""
        relevant_logs = []
        for log in logs:
            if query.lower() in log.get('message', '').lower():
                relevant_logs.append(log)
                if len(relevant_logs) >= 3:
                    break
        return relevant_logs

    def find_relevant_tasks(self, query: str, tasks: list) -> list:
        """Find relevant automation tasks using semantic search"""
        relevant_tasks = []
        for task in tasks:
            if query.lower() in task.get('description', '').lower():
                relevant_tasks.append(task)
                if len(relevant_tasks) >= 3:
                    break
        return relevant_tasks