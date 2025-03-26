import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from services.ticket_analysis_service import TicketAnalysisService
import pandas as pd
from typing import Dict, Any
from datetime import datetime

class TicketAnalyzer:
    def __init__(self):
        self.service = TicketAnalysisService()
        
    def render(self):
        """Render the ticket analysis interface"""
        st.title("Ticket Analysis Dashboard")
        
        # Load data
        df = self.service.load_sample_data()
        
        # Create tabs for different analysis views
        tab1, tab2, tab3 = st.tabs(["Overview", "Trend Analysis", "Ticket Analysis"])
        
        with tab1:
            self._render_overview(df)
            
        with tab2:
            self._render_trend_analysis(df)
            
        with tab3:
            self._render_ticket_analysis(df)
    
    def _render_overview(self, df: pd.DataFrame):
        """Render overview statistics and insights"""
        st.header("Overview")
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tickets", len(df))
            
        with col2:
            open_tickets = len(df[df['status'] == 'Open'])
            st.metric("Open Tickets", open_tickets)
            
        with col3:
            critical_tickets = len(df[df['priority'] == 'Critical'])
            st.metric("Critical Tickets", critical_tickets)
            
        with col4:
            avg_resolution = df['resolution_time'].mean()
            st.metric("Avg Resolution Time (days)", f"{avg_resolution:.1f}")
        
        # Display insights
        st.subheader("Key Insights")
        insights = self.service.generate_insights(df)
        for insight in insights:
            st.info(insight)
        
        # Display priority distribution
        st.subheader("Priority Distribution")
        priority_dist = df['priority'].value_counts()
        fig = px.pie(
            values=priority_dist.values,
            names=priority_dist.index,
            title="Ticket Priority Distribution"
        )
        st.plotly_chart(fig)
    
    def _render_trend_analysis(self, df: pd.DataFrame):
        """Render trend analysis visualizations"""
        st.header("Trend Analysis")
        
        # Get trend data
        trends = self.service.analyze_ticket_trends(df)
        
        # Monthly ticket trends
        st.subheader("Monthly Ticket Volume")
        monthly_counts = trends['monthly_counts']
        # Convert Period to string for plotting
        monthly_counts['month'] = monthly_counts['month'].astype(str)
        fig = px.line(
            monthly_counts,
            x='month',
            y='count',
            title="Monthly Ticket Volume Trend"
        )
        st.plotly_chart(fig)
        
        # Resolution time by priority
        st.subheader("Average Resolution Time by Priority")
        resolution_data = pd.DataFrame({
            'Priority': trends['avg_resolution_time'].keys(),
            'Days': trends['avg_resolution_time'].values()
        })
        fig = px.bar(
            resolution_data,
            x='Priority',
            y='Days',
            title="Average Resolution Time by Priority"
        )
        st.plotly_chart(fig)
        
        # Component distribution
        st.subheader("Tickets by Component")
        component_dist = pd.DataFrame({
            'Component': trends['component_distribution'].keys(),
            'Count': trends['component_distribution'].values()
        })
        fig = px.bar(
            component_dist,
            x='Component',
            y='Count',
            title="Ticket Distribution by Component"
        )
        st.plotly_chart(fig)
    
    def _render_ticket_analysis(self, df: pd.DataFrame):
        """Render detailed ticket analysis"""
        st.header("Ticket Details")
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df['status'].unique(),
                default=df['status'].unique()
            )
        with col2:
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=df['priority'].unique(),
                default=df['priority'].unique()
            )
        with col3:
            component_filter = st.multiselect(
                "Filter by Component",
                options=df['component'].unique(),
                default=df['component'].unique()
            )
        
        # Apply filters
        filtered_df = df[
            (df['status'].isin(status_filter)) &
            (df['priority'].isin(priority_filter)) &
            (df['component'].isin(component_filter))
        ]
        
        # Display ticket details in a table
        st.subheader("Ticket List")
        
        # Format the DataFrame for display
        display_df = filtered_df.copy()
        display_df['created_date'] = display_df['created_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Add color coding for priority
        def get_priority_color(priority):
            colors = {
                'Critical': 'red',
                'High': 'orange',
                'Medium': 'yellow',
                'Low': 'green'
            }
            return colors.get(priority, 'gray')
        
        # Display tickets in expandable sections
        for _, ticket in display_df.iterrows():
            with st.expander(f"{ticket['ticket_id']} - {ticket['title']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Status:** {ticket['status']}")
                    st.markdown(f"**Priority:** <span style='color: {get_priority_color(ticket['priority'])}'>{ticket['priority']}</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**Created:** {ticket['created_date']}")
                    st.markdown(f"**Component:** {ticket['component']}")
                with col3:
                    st.markdown(f"**Assignee:** {ticket['assignee']}")
                    st.markdown(f"**Resolution Time:** {ticket['resolution_time']} days")
                
                st.markdown("**Description:**")
                st.markdown(ticket['description'])
                
                # Add resolution comment if available
                if 'resolution_comment' in ticket and ticket['resolution_comment']:
                    st.markdown("**Resolution Comment:**")
                    st.markdown(ticket['resolution_comment'])
                
                # Add server details if available
                if 'server_details' in ticket and ticket['server_details']:
                    st.markdown("**Server Details:**")
                    st.markdown(ticket['server_details'])
                
                st.markdown("---") 