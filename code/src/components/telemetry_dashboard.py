import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.telemetry_service import TelemetryService
from utils.alerts_service import AlertsService
from services.data_service import DataService
from datetime import datetime, timedelta

class TelemetryDashboard:
    def __init__(self):
        self.telemetry_service = TelemetryService()
        self.alerts_service = AlertsService()
        self.data_service = DataService()

    def render(self):
        st.header("Telemetry Dashboard")

        # CI Selection
        selected_ci = st.selectbox(
            "Select Configuration Item",
            self.telemetry_service.get_ci_list()
        )

        # Time range selection
        time_range = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 24 Hours", "Last 7 Days"],
            index=0
        )

        # Layout
        col1, col2 = st.columns([2, 1])

        with col1:
            self.render_metrics_section(selected_ci, time_range)

        with col2:
            self.render_alerts_section(selected_ci)

    def render_metrics_section(self, ci_id: str, time_range: str):
        """Render metrics visualizations"""
        st.subheader("System Metrics")

        # Get CI details and metrics
        ci_details = self.telemetry_service.get_ci_details(ci_id)

        # CPU Usage
        cpu_data = ci_details["metrics"]["cpu"]
        fig_cpu = self.create_metric_chart(
            cpu_data,
            "CPU Usage Over Time",
            "CPU Usage (%)"
        )
        st.plotly_chart(fig_cpu, use_container_width=True)

        # Memory Usage
        memory_data = ci_details["metrics"]["memory"]
        fig_memory = self.create_metric_chart(
            memory_data,
            "Memory Usage Over Time",
            "Memory Usage (%)"
        )
        st.plotly_chart(fig_memory, use_container_width=True)

        # Disk Usage
        disk_data = ci_details["metrics"]["disk"]
        fig_disk = self.create_metric_chart(
            disk_data,
            "Disk Usage Over Time",
            "Disk Usage (%)"
        )
        st.plotly_chart(fig_disk, use_container_width=True)

    def render_alerts_section(self, ci_id: str):
        """Render alerts section"""
        st.subheader("Active Alerts")

        # Get alert statistics
        stats = self.alerts_service.get_alert_stats()
        
        # Display alert stats in columns
        stat_cols = st.columns(3)
        with stat_cols[0]:
            st.metric("Active Alerts", stats["active"])
        with stat_cols[1]:
            st.metric("Critical", stats["critical"])
        with stat_cols[2]:
            st.metric("Warnings", stats["warning"])

        # Get and display active alerts for selected CI
        alerts = self.alerts_service.get_active_alerts(ci_id)
        
        for alert in alerts:
            severity_color = {
                "critical": "red",
                "warning": "orange",
                "info": "blue"
            }.get(alert["severity"], "gray")

            with st.expander(f"{alert['title']} ({alert['severity'].upper()})"):
                st.markdown(
                    f"""
                    <div style='padding: 10px; border-left: 5px solid {severity_color};'>
                        <p>{alert['description']}</p>
                        <small>Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button(f"Acknowledge Alert {alert['id']}", key=f"ack_{alert['id']}"):
                    if self.alerts_service.acknowledge_alert(alert['id']):
                        st.success("Alert acknowledged successfully!")
                        st.rerun()

    def create_metric_chart(self, data: pd.DataFrame, title: str, y_axis_title: str) -> go.Figure:
        """Create a metric chart using Plotly"""
        fig = px.line(
            data,
            x="timestamp",
            y="value",
            title=title
        )
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title=y_axis_title,
            height=300
        )
        
        return fig

    def filter_by_timerange(self, data: pd.DataFrame, time_range: str) -> pd.DataFrame:
        # Implementation of filter_by_timerange method
        pass

    def get_recent_alerts(self, data: pd.DataFrame) -> list:
        # Implementation of get_recent_alerts method
        pass

    def render_alert_card(self, alert: dict):
        # Implementation of render_alert_card method
        pass 