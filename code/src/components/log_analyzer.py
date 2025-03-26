import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from services.log_service import LogService
from services.agent_service import AgentService
from typing import List, Dict
import json
import asyncio

class LogAnalyzer:
    def __init__(self):
        self.log_service = LogService()
        self.agent_service = AgentService()
        
    def render(self):
        st.header("Log Analysis Dashboard")
        
        # Create tabs for different sections
        tabs = st.tabs([
            "Log Explorer",
            "Log Analysis",
            "Anomaly Detection",
            "Insights"
        ])
        
        with tabs[0]:
            self.render_log_explorer()
            
        with tabs[1]:
            self.render_log_analysis()
            
        with tabs[2]:
            self.render_anomaly_detection()
            
        with tabs[3]:
            self.render_insights()
            
    def render_log_explorer(self):
        """Render log exploration interface"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Application selection
            applications = ["web_server", "database", "auth_service", "api_gateway"]
            selected_app = st.selectbox("Select Application", applications, key="log_explorer_app")
            
        with col2:
            # Server selection
            servers = ["server-01", "server-02", "server-03", "server-04"]
            selected_server = st.selectbox("Select Server", servers, key="log_explorer_server")
            
        # Time range selection
        time_range = st.select_slider(
            "Time Range",
            options=["1h", "6h", "12h", "24h", "7d"],
            value="24h",
            key="log_explorer_time_range"
        )
        
        # Log level filter
        log_levels = ["ALL", "INFO", "WARNING", "ERROR", "DEBUG"]
        selected_level = st.selectbox("Log Level", log_levels, key="log_explorer_level")
        
        # Get logs based on filters
        end_time = datetime.now()
        start_time = end_time - self._get_timedelta(time_range)
        
        logs = self.log_service.get_logs(
            application=selected_app,
            server=selected_server,
            start_time=start_time,
            end_time=end_time,
            log_level=None if selected_level == "ALL" else selected_level
        )
        
        # Display log summary
        summary = self.log_service.get_log_summary(selected_app, selected_server, time_range)
        
        # Show summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Logs", summary["total_logs"])
        with col2:
            st.metric("Errors", summary["error_count"], delta_color="inverse")
        with col3:
            st.metric("Warnings", summary["warning_count"])
        with col4:
            st.metric("Avg Response Time", f"{summary['avg_response_time']:.1f}ms")
            
        # Log visualization
        st.subheader("Log Timeline")
        if logs:
            df = pd.DataFrame(logs)
            fig = px.scatter(
                df,
                x="timestamp",
                y="level",
                color="level",
                hover_data=["message", "trace_id", "user_id", "duration_ms"],
                title="Log Timeline"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Log table
            st.subheader("Log Details")
            st.dataframe(
                df[[
                    "timestamp", "level", "message", "server",
                    "trace_id", "user_id", "duration_ms", "status_code"
                ]].sort_values("timestamp", ascending=False).reset_index(drop=True)
            )
        else:
            st.info("No logs found for the selected criteria")
            
    def render_log_analysis(self):
        """Render log analysis interface"""
        st.subheader("Log Analysis")
        
        # Application and server selection
        col1, col2 = st.columns(2)
        with col1:
            applications = ["web_server", "database", "auth_service", "api_gateway"]
            selected_app = st.selectbox("Select Application", applications, key="log_analysis_app")
        with col2:
            servers = ["server-01", "server-02", "server-03", "server-04"]
            selected_server = st.selectbox("Select Server", servers, key="log_analysis_server")
            
        # Analysis type selection
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Error Patterns", "Performance Analysis", "User Behavior", "System Health"],
            key="log_analysis_type"
        )
        
        if st.button("Run Analysis", key="log_analysis_button"):
            with st.spinner("Analyzing logs..."):
                # Get logs for analysis
                logs = self.log_service.get_logs(
                    application=selected_app,
                    server=selected_server,
                    start_time=datetime.now() - timedelta(days=7)
                )
                
                # Create analysis prompt
                prompt = self._create_analysis_prompt(analysis_type, logs)
                
                # Get AI analysis
                try:
                    analysis = asyncio.run(
                        self.agent_service.analyze_logs(prompt, logs)
                    )
                    
                    # Display analysis results
                    st.markdown("### Analysis Results")
                    
                    if 'error' in analysis:
                        st.error(f"Error during analysis: {analysis['error']}")
                    else:
                        # Display summary
                        st.markdown("#### Summary")
                        st.markdown(analysis['summary'])
                        
                        # Display key events
                        if analysis['key_events']:
                            st.markdown("#### Key Events")
                            for event in analysis['key_events']:
                                st.markdown(f"- {event}")
                        
                        # Display issues
                        if analysis['issues']:
                            st.markdown("#### Potential Issues")
                            for issue in analysis['issues']:
                                st.markdown(f"- {issue}")
                        
                        # Display recommendations
                        if analysis['recommendations']:
                            st.markdown("#### Recommendations")
                            for rec in analysis['recommendations']:
                                st.markdown(f"- {rec}")
                        
                        # Display timestamp
                        st.markdown(f"*Analysis generated at: {analysis['timestamp']}*")
                        
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                
    def render_anomaly_detection(self):
        """Render anomaly detection interface"""
        st.subheader("Anomaly Detection")
        
        # Application and server selection
        col1, col2 = st.columns(2)
        with col1:
            applications = ["web_server", "database", "auth_service", "api_gateway"]
            selected_app = st.selectbox("Select Application", applications, key="anomaly_detection_app")
        with col2:
            servers = ["server-01", "server-02", "server-03", "server-04"]
            selected_server = st.selectbox("Select Server", servers, key="anomaly_detection_server")
            
        # Anomaly detection parameters
        sensitivity = st.slider("Detection Sensitivity", 0.1, 1.0, 0.5, key="anomaly_detection_sensitivity")
        time_window = st.select_slider(
            "Time Window",
            options=["1h", "6h", "12h", "24h", "7d"],
            value="24h",
            key="anomaly_detection_time_window"
        )
        
        if st.button("Detect Anomalies", key="anomaly_detection_button"):
            with st.spinner("Detecting anomalies..."):
                # Get logs for anomaly detection
                logs = self.log_service.get_logs(
                    application=selected_app,
                    server=selected_server,
                    start_time=datetime.now() - self._get_timedelta(time_window)
                )
                
                # Create anomaly detection prompt
                prompt = self._create_anomaly_prompt(logs, sensitivity)
                
                # Get AI analysis
                anomalies = asyncio.run(
                    self.agent_service.detect_anomalies(prompt, logs)
                )
                
                # Display anomalies
                st.markdown("### Detected Anomalies")
                
                if not anomalies:
                    st.info("No anomalies detected in the selected time window.")
                else:
                    for anomaly in anomalies:
                        with st.expander(f"{anomaly['type'].title()} - {anomaly['severity'].upper()}", expanded=True):
                            st.markdown(f"**Description:** {anomaly['description']}")
                            st.markdown(f"**Timestamp:** {anomaly['timestamp']}")
                            st.markdown(f"**Affected Components:** {', '.join(anomaly['affected_components'])}")
                            st.markdown("**Recommendations:**")
                            for rec in anomaly['recommendations']:
                                st.markdown(f"- {rec}")
                
    def render_insights(self):
        """Render AI-powered insights"""
        st.header("AI-Powered Insights")
        
        # Application and server selection
        col1, col2 = st.columns(2)
        with col1:
            applications = ["web_server", "database", "auth_service", "api_gateway", "all"]
            application = st.selectbox(
                "Select Application",
                applications,
                index=applications.index(st.session_state.get('selected_application', 'all')),
                key="insights_application"
            )
        with col2:
            servers = ["server-01", "server-02", "server-03", "server-04", "all"]
            server = st.selectbox(
                "Select Server",
                servers,
                index=servers.index(st.session_state.get('selected_server', 'all')),
                key="insights_server"
            )
        
        # Get time range
        time_range = st.selectbox(
            "Select Time Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom Range"],
            key="insights_time_range"
        )
        
        # Initialize end_time as datetime
        end_time = datetime.now()
        
        if time_range == "Custom Range":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
                # Convert date to datetime with time set to start of day
                start_time = datetime.combine(start_date, datetime.min.time())
            with col2:
                end_date = st.date_input("End Date")
                # Convert date to datetime with time set to end of day
                end_time = datetime.combine(end_date, datetime.max.time())
        else:
            if time_range == "Last 24 Hours":
                start_time = end_time - timedelta(days=1)
            elif time_range == "Last 7 Days":
                start_time = end_time - timedelta(days=7)
            else:  # Last 30 Days
                start_time = end_time - timedelta(days=30)
        
        # Get logs with filters
        logs = self.log_service.get_logs(
            application=application if application != "all" else "all",
            server=server if server != "all" else "all",
            start_time=start_time,
            end_time=end_time
        )
        
        if not logs:
            st.warning("No logs found for the selected criteria")
            return
        
        # Convert logs to DataFrame for easier analysis
        df = pd.DataFrame(logs)
        
        # Ensure timestamp is datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Display log statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Logs", len(df))
        with col2:
            error_rate = (len(df[df['level'] == 'ERROR']) / len(df)) * 100 if len(df) > 0 else 0
            st.metric("Error Rate", f"{error_rate:.1f}%")
        with col3:
            st.metric("Unique Components", df['component'].nunique())
        with col4:
            time_range_str = f"{df['timestamp'].min().strftime('%Y-%m-%d')} to {df['timestamp'].max().strftime('%Y-%m-%d')}"
            st.metric("Time Range", time_range_str)
        
        # Log Level Distribution
        st.subheader("Log Level Distribution")
        level_counts = df['level'].value_counts()
        level_data = pd.DataFrame({
            'Level': level_counts.index,
            'Count': level_counts.values
        })
        
        # Create pie chart for log levels
        fig_levels = px.pie(
            level_data,
            values='Count',
            names='Level',
            title="Distribution of Log Levels",
            color='Level',
            color_discrete_map={
                'ERROR': 'red',
                'WARNING': 'orange',
                'INFO': 'blue',
                'DEBUG': 'gray'
            }
        )
        st.plotly_chart(fig_levels, use_container_width=True)
        
        # Component Distribution
        st.subheader("Component Distribution")
        component_counts = df['component'].value_counts()
        component_data = pd.DataFrame({
            'Component': component_counts.index,
            'Count': component_counts.values
        })
        
        # Create bar chart for components
        fig_components = px.bar(
            component_data,
            x='Component',
            y='Count',
            title="Log Distribution by Component",
            color='Component'
        )
        fig_components.update_layout(
            xaxis_title="Component",
            yaxis_title="Number of Logs",
            showlegend=False
        )
        st.plotly_chart(fig_components, use_container_width=True)
        
        # AI Analysis
        st.subheader("AI Analysis")
        analysis_prompt = st.text_area(
            "Enter analysis prompt",
            "Analyze these logs and provide insights about system performance, potential issues, and recommendations.",
            key="analysis_prompt"
        )
        
        if st.button("Generate Analysis", key="generate_analysis"):
            with st.spinner("Generating insights..."):
                analysis = asyncio.run(
                    self.agent_service.analyze_logs(analysis_prompt, logs)
                )
                
                if 'error' in analysis:
                    st.error(f"Error generating analysis: {analysis['error']}")
                else:
                    st.markdown(analysis['summary'])
                    
                    # Display key events
                    if analysis.get('key_events'):
                        st.markdown("#### Key Events")
                        for event in analysis['key_events']:
                            st.markdown(f"- {event}")
                    
                    # Display issues
                    if analysis.get('issues'):
                        st.markdown("#### Potential Issues")
                        for issue in analysis['issues']:
                            st.markdown(f"- {issue}")
                    
                    # Display recommendations
                    if analysis.get('recommendations'):
                        st.markdown("#### Recommendations")
                        for rec in analysis['recommendations']:
                            st.markdown(f"- {rec}")
                
    def _get_timedelta(self, time_range: str) -> timedelta:
        """Convert time range string to timedelta"""
        if time_range == "1h":
            return timedelta(hours=1)
        elif time_range == "6h":
            return timedelta(hours=6)
        elif time_range == "12h":
            return timedelta(hours=12)
        elif time_range == "24h":
            return timedelta(days=1)
        elif time_range == "7d":
            return timedelta(days=7)
        return timedelta(hours=1)
        
    def _create_analysis_prompt(self, analysis_type: str, logs: List[Dict]) -> str:
        """Create prompt for log analysis"""
        return f"""
        Analyze the following logs for {analysis_type}:
        
        Log Summary:
        - Total entries: {len(logs)}
        - Time range: {logs[0]['timestamp']} to {logs[-1]['timestamp']}
        - Log levels: {set(log['level'] for log in logs)}
        
        Please provide:
        1. Key patterns and trends
        2. Potential issues or concerns
        3. Recommendations for improvement
        """
        
    def _create_anomaly_prompt(self, logs: List[Dict], sensitivity: float) -> str:
        """Create prompt for anomaly detection"""
        return f"""
        Detect anomalies in the following logs with sensitivity {sensitivity}:
        
        Log Summary:
        - Total entries: {len(logs)}
        - Time range: {logs[0]['timestamp']} to {logs[-1]['timestamp']}
        
        Please identify:
        1. Unusual patterns or spikes
        2. Unexpected error rates
        3. Performance anomalies
        4. Security concerns
        """ 
