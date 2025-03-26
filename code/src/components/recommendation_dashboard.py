import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import plotly.express as px
import plotly.graph_objects as go
from services.recommendation_service import RecommendationService

class RecommendationDashboard:
    def __init__(self, recommendation_service: RecommendationService):
        self.recommendation_service = recommendation_service

    def render(self):
        st.title("Recommendation Dashboard")
        
        # Sidebar filters
        with st.sidebar:
            st.header("Filters")
            time_range = st.selectbox(
                "Time Range",
                ["Last 24 hours", "Last 7 days", "Last 30 days", "Custom Range"]
            )
            
            if time_range == "Custom Range":
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
            else:
                days = {
                    "Last 24 hours": 1,
                    "Last 7 days": 7,
                    "Last 30 days": 30
                }
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days[time_range])
            
            priority_filter = st.multiselect(
                "Priority",
                ["High", "Medium", "Low"],
                default=["High", "Medium", "Low"]
            )
            
            type_filter = st.multiselect(
                "Recommendation Type",
                ["Performance", "Security", "Cost", "Reliability"],
                default=["Performance", "Security", "Cost", "Reliability"]
            )

        # Main content
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Recommendations",
                len(self.recommendation_service.get_recommendations(start_date, end_date))
            )
        
        with col2:
            high_priority = len([
                r for r in self.recommendation_service.get_recommendations(start_date, end_date)
                if r["priority"] == "High"
            ])
            st.metric("High Priority", high_priority)
        
        with col3:
            accuracy_metrics = self.recommendation_service.get_accuracy_metrics()
            st.metric("Accuracy Score", f"{accuracy_metrics['f1_score']:.1%}")

        # Active Recommendations
        st.header("Active Recommendations")
        recommendations = self.recommendation_service.get_recommendations(start_date, end_date)
        
        for rec in recommendations:
            if rec["priority"] in priority_filter and rec["type"] in type_filter:
                with st.expander(f"{rec['title']} ({rec['priority']} Priority)"):
                    st.write(rec["description"])
                    st.write(f"**Impact:** {rec['impact']}")
                    st.write(f"**Created:** {rec['created_at']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Mark as Implemented", key=f"implement_{rec['id']}"):
                            self.recommendation_service.mark_recommendation_implemented(rec["id"])
                            st.success("Recommendation marked as implemented!")
                    with col2:
                        if st.button("Mark as Effective", key=f"effective_{rec['id']}"):
                            self.recommendation_service.mark_recommendation_effective(rec["id"])
                            st.success("Recommendation marked as effective!")

        # Trends and Patterns
        st.header("Trends and Patterns")
        
        # Get telemetry data
        telemetry_data = self.recommendation_service.get_telemetry_data(start_date, end_date)
        
        if telemetry_data:
            df = pd.DataFrame(telemetry_data)
            
            # Create trend visualization
            fig = px.line(df, x='timestamp', y='value', title='System Metrics Trend')
            st.plotly_chart(fig)
            
            # Create pattern visualization
            fig = px.scatter(df, x='timestamp', y='value', title='Metric Patterns')
            st.plotly_chart(fig)

        # Incident Patterns
        st.header("Incident Patterns")
        incident_data = self.recommendation_service.get_incident_patterns(start_date, end_date)
        
        if incident_data:
            df = pd.DataFrame(incident_data)
            
            # Create heatmap of incident patterns
            fig = go.Figure(data=go.Heatmap(
                z=df['count'].values.reshape(-1, 24),
                x=df['hour'].unique(),
                y=df['day'].unique()
            ))
            fig.update_layout(title='Incident Patterns by Hour and Day')
            st.plotly_chart(fig)

        # Accuracy Metrics
        st.header("Recommendation Accuracy")
        accuracy_metrics = self.recommendation_service.get_accuracy_metrics()
        
        if accuracy_metrics:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=accuracy_metrics['precision'],
                    title={'text': "Precision"},
                    gauge={'axis': {'range': [0, 1]}}
                ))
                st.plotly_chart(fig)
            
            with col2:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=accuracy_metrics['recall'],
                    title={'text': "Recall"},
                    gauge={'axis': {'range': [0, 1]}}
                ))
                st.plotly_chart(fig)
            
            with col3:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=accuracy_metrics['f1_score'],
                    title={'text': "F1 Score"},
                    gauge={'axis': {'range': [0, 1]}}
                ))
                st.plotly_chart(fig) 