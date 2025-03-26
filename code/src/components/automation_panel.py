import streamlit as st
from utils.ansible_service import AnsibleService
from utils.health_check_service import HealthCheckService
from services.agent_service import AgentService
from datetime import datetime, timedelta
import json
import asyncio
import time
from utils.log_service import LogService
from typing import Dict, Any
import logging

class AutomationPanel:
    def __init__(self):
        """Initialize the Automation Panel."""
        # Initialize services
        self.ansible_service = AnsibleService()
        self.health_check_service = HealthCheckService()
        self.agent_service = AgentService()
        self.log_service = LogService()
        
        # Initialize active tasks list
        self.active_tasks = []
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Add console handler if not already added
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def render(self):
        st.header("Automation Panel")

        # Create tabs for different sections
        tabs = st.tabs([
            "Agent Tasks",
            "Health Checks",
            "Ansible Playbooks",
            "Task History"
        ])

        with tabs[0]:
            self.render_agent_tasks()

        with tabs[1]:
            self.render_health_checks()

        with tabs[2]:
            self.render_playbooks_section()

        with tabs[3]:
            self.render_task_history()

    def render_agent_tasks(self):
        """Render agent tasks section"""
        st.subheader("Intelligent Agent Tasks")

        # Create new task
        with st.expander("Create New Task", expanded=True):
            with st.form("create_agent_task_form"):
                task_description = st.text_area(
                    "Task Description",
                    placeholder="Describe what you want the agent to do..."
                )
                context = st.text_area(
                    "Context (JSON)",
                    placeholder='{"key": "value"}'
                )
                
                submitted = st.form_submit_button("Create Task")
                
                if submitted:
                    try:
                        ctx = json.loads(context) if context else None
                        asyncio.run(self.create_task(task_description, ctx))
                    except json.JSONDecodeError:
                        st.error("Invalid JSON in context")
                    except Exception as e:
                        st.error(f"Error creating task: {str(e)}")

        # Active tasks
        st.subheader("Active Tasks")
        active_tasks = self.agent_service.get_active_tasks()
        
        if not active_tasks:
            st.info("No active tasks")
            return

        for task in active_tasks:
            with st.expander(f"Task {task['task_id']} - {task['status']}"):
                # Task details
                st.json(task)

                # Execute and Archive buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Execute Task - {task['task_id']}"):
                        self.execute_task(task['task_id'])
                
                with col2:
                    if st.button(f"Archive Task - {task['task_id']}"):
                        self.agent_service.archive_task(task['task_id'])
                        st.success(f"Task {task['task_id']} archived")
                        st.rerun()

    def render_health_checks(self):
        """Render health checks section"""
        st.subheader("System Health Checks")

        # Create two columns for controls
        control_col1, control_col2 = st.columns([2, 1])
        
        with control_col1:
            # System selection
            selected_system = st.selectbox(
                "Select System",
                self.health_check_service.get_available_systems()
            )
        
        with control_col2:
            # Auto-refresh toggle
            auto_refresh = st.checkbox("Auto-refresh", value=False)
            if auto_refresh:
                st.empty()
                time_options = {
                    "30 seconds": 30,
                    "1 minute": 60,
                    "5 minutes": 300
                }
                refresh_interval = st.selectbox(
                    "Refresh Interval",
                    options=list(time_options.keys()),
                    index=0
                )
                if st.button("Stop Auto-refresh"):
                    auto_refresh = False

        # Create a form for health check
        with st.form("health_check_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("Run health check for selected system")
            with col2:
                submitted = st.form_submit_button("Run Health Check", use_container_width=True)
            
            if submitted or auto_refresh:
                try:
                    results = self.health_check_service.run_check(selected_system)
                    st.success("Health check completed!")
                    
                    # Display results in a more user-friendly format
                    if isinstance(results, dict):
                        # Create columns for status overview with improved styling
                        st.markdown("""
                            <style>
                            .status-metric {
                                padding: 10px;
                                border-radius: 5px;
                                margin: 5px;
                            }
                            </style>
                        """, unsafe_allow_html=True)
                        
                        status_cols = st.columns(4)
                        with status_cols[0]:
                            total_checks = len(results.get('checks', []))
                            st.metric(
                                "Total Checks",
                                total_checks,
                                help="Total number of system components checked"
                            )
                        with status_cols[1]:
                            passed = sum(1 for check in results.get('checks', []) if check.get('status') == 'healthy')
                            st.metric(
                                "Healthy",
                                passed,
                                delta=f"{(passed/total_checks)*100:.1f}%" if total_checks > 0 else "0%",
                                delta_color="normal",
                                help="Components in healthy state"
                            )
                        with status_cols[2]:
                            warnings = sum(1 for check in results.get('checks', []) if check.get('status') == 'warning')
                            st.metric(
                                "Warnings",
                                warnings,
                                delta=warnings if warnings > 0 else None,
                                delta_color="inverse",
                                help="Components with warnings"
                            )
                        with status_cols[3]:
                            failed = sum(1 for check in results.get('checks', []) if check.get('status') == 'critical')
                            st.metric(
                                "Critical",
                                failed,
                                delta=failed if failed > 0 else None,
                                delta_color="inverse",
                                help="Components in critical state"
                            )

                        # Display system checks
                        st.markdown("### System Health Details")
                        
                        # Display checks
                        for check in results.get('checks', []):
                            status = check.get('status', 'unknown')
                            color = {
                                'healthy': 'green',
                                'warning': 'orange',
                                'critical': 'red',
                                'unknown': 'gray'
                            }.get(status, 'gray')
                            
                            with st.expander(f"{check.get('name', 'Unknown Check')}", expanded=(status in ['critical', 'warning'])):
                                st.markdown(f"""
                                    <div style='padding: 10px; border-left: 3px solid {color}; margin-bottom: 10px;'>
                                        <div style='color: {color}; font-weight: bold;'>Status: {status.upper()}</div>
                                        <div style='margin-top: 5px;'><strong>Value:</strong> {check.get('value', 'N/A')}</div>
                                        <div style='margin-top: 5px;'><strong>Threshold:</strong> {check.get('threshold', 'N/A')}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                        
                        # Display services
                        if results.get('services'):
                            st.markdown("### Service Status")
                            for service in results['services']:
                                status = service.get('status', 'unknown')
                                color = {
                                    'running': 'green',
                                    'warning': 'orange',
                                    'stopped': 'red',
                                    'unknown': 'gray'
                                }.get(status, 'gray')
                                
                                with st.expander(f"{service.get('name', 'Unknown Service')}", expanded=(status != 'running')):
                                    st.markdown(f"""
                                        <div style='padding: 10px; border-left: 3px solid {color}; margin-bottom: 10px;'>
                                            <div style='color: {color}; font-weight: bold;'>Status: {status.upper()}</div>
                                            <div style='margin-top: 5px;'><strong>Uptime:</strong> {service.get('uptime', 'N/A')}</div>
                                            <div style='margin-top: 5px;'><strong>Memory Usage:</strong> {service.get('memory_usage', 'N/A')}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                        
                        # Add timestamp of last check
                        st.markdown("---")
                        timestamp = results.get('timestamp')
                        if isinstance(timestamp, datetime):
                            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            timestamp_str = str(timestamp) if timestamp else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        st.markdown(f"*Last checked: {timestamp_str}*")
                        
                    else:
                        st.warning("No health check data available")
                        
                except Exception as e:
                    st.error(f"Error running health check: {str(e)}")
                    
        if auto_refresh:
            time.sleep(time_options[refresh_interval])
            st.rerun()

    def render_playbooks_section(self):
        """Render available playbooks section"""
        st.subheader("Available Playbooks")

        # Get available playbooks
        playbooks = self.ansible_service.get_available_playbooks()

        # Display each playbook as an expander
        for playbook in playbooks:
            with st.expander(f"{playbook['name']} - {playbook['description']}"):
                # Create form for playbook parameters
                form_id = f"playbook_form_{playbook['id']}"
                with st.form(form_id):
                    params = {}
                    
                    # Generate input fields for required parameters
                    for param in playbook["params"]:
                        param_key = f"param_{playbook['id']}_{param}"
                        params[param] = st.text_input(
                            f"{param.replace('_', ' ').title()}"
                        )

                    # Submit button
                    submitted = st.form_submit_button("Run Playbook")
                    
                    if submitted:
                        try:
                            # Validate all parameters are provided
                            if all(params.values()):
                                result = self.ansible_service.run_playbook(
                                    playbook["id"],
                                    params
                                )
                                st.success("Playbook executed successfully!")
                                st.json(result)
                            else:
                                st.error("Please fill in all required parameters")
                        except Exception as e:
                            st.error(f"Error executing playbook: {str(e)}")

    def render_task_history(self):
        """Render task history section"""
        st.subheader("Task History")

        # Initialize task history in session state if not exists
        if 'task_history' not in st.session_state:
            st.session_state['task_history'] = self.agent_service.get_task_history()

        # Get task history from session state
        history = st.session_state['task_history']

        if not history:
            st.info("No task history found")
            return

        # Display tasks in expandable sections
        for task in history:
            # Format timestamps
            created_at = task.get('created_at', '')
            completed_at = task.get('completed_at', '')
            if isinstance(created_at, datetime):
                created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(completed_at, datetime):
                completed_at = completed_at.strftime('%Y-%m-%d %H:%M:%S')

            # Calculate completion time
            if isinstance(task.get('created_at'), datetime) and isinstance(task.get('completed_at'), datetime):
                duration = task['completed_at'] - task['created_at']
                duration_str = f"{duration.total_seconds():.1f} seconds"
            else:
                duration_str = "N/A"

            # Create expander title with task details
            expander_title = f"""
            Task {task['task_id']} - {task['status']}
            Created: {created_at} | Completed: {completed_at} | Duration: {duration_str}
            """

            with st.expander(expander_title):
                # Task details
                st.markdown("### Task Details")
                st.json({
                    "description": task.get('description', ''),
                    "context": task.get('context', {}),
                    "status": task.get('status', ''),
                    "created_at": created_at,
                    "completed_at": completed_at,
                    "duration": duration_str
                })

                # Steps
                if task.get('steps'):
                    st.markdown("### Execution Steps")
                    for step in task['steps']:
                        step_status = step.get('status', '')
                        step_color = {
                            'completed': 'green',
                            'failed': 'red',
                            'pending': 'gray',
                            'running': 'orange'
                        }.get(step_status, 'gray')

                        st.markdown(f"""
                            <div style='padding: 10px; border-left: 3px solid {step_color}; margin-bottom: 10px;'>
                                <div style='color: {step_color}; font-weight: bold;'>Step: {step.get('id', 'Unknown')}</div>
                                <div style='margin-top: 5px;'><strong>Description:</strong> {step.get('description', 'N/A')}</div>
                                <div style='margin-top: 5px;'><strong>Status:</strong> {step_status.upper()}</div>
                                <div style='margin-top: 5px;'><strong>Result:</strong> {step.get('result', 'N/A')}</div>
                            </div>
                        """, unsafe_allow_html=True)

    def render_action_status(self, action):
        """Render status for a single action"""
        status_color = {
            "success": "green",
            "failed": "red",
            "running": "blue"
        }.get(action["status"], "gray")

        st.markdown(
            f"""
            <div style='padding: 10px; border-left: 5px solid {status_color};'>
                <h4>{action['playbook_id']}</h4>
                <p>Status: {action['status']}</p>
                <small>Time: {action['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render_custom_automation(self):
        """Render custom automation section"""
        st.subheader("Custom Automation")
        st.info("Custom automation features coming soon!")

    def render_ansible_automation(self):
        st.subheader("Ansible Automation")
        
        # Playbook selection
        playbook = st.selectbox(
            "Select Playbook",
            self.ansible_service.get_available_playbooks()
        )

        # Parameters input
        params = {}
        for param in self.ansible_service.get_playbook_params(playbook):
            params[param] = st.text_input(f"Parameter: {param}")

        if st.button("Run Playbook"):
            with st.spinner("Executing playbook..."):
                result = self.ansible_service.run_playbook(playbook, params)
                st.json(result)

    def run_health_check(self):
        """Run health check on selected server"""
        try:
            # Get server selection
            server = st.session_state.get('selected_server', 'server-01')
            
            # Get logs for the last 24 hours
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)
            
            # Get logs with proper datetime objects
            logs = self.log_service.get_logs(
                server=server,
                start_time=start_time,
                end_time=end_time
            )
            
            if not logs:
                st.warning("No logs found for the selected server in the last 24 hours")
                return
            
            # Analyze logs
            error_count = sum(1 for log in logs if log.get('level', '').upper() == 'ERROR')
            warning_count = sum(1 for log in logs if log.get('level', '').upper() == 'WARNING')
            total_logs = len(logs)
            
            # Calculate metrics
            error_rate = error_count / total_logs if total_logs > 0 else 0
            warning_rate = warning_count / total_logs if total_logs > 0 else 0
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Logs", total_logs)
            with col2:
                st.metric("Error Rate", f"{error_rate*100:.1f}%")
            with col3:
                st.metric("Warning Rate", f"{warning_rate*100:.1f}%")
            
            # Display recent errors
            if error_count > 0:
                st.subheader("Recent Errors")
                error_logs = [log for log in logs if log.get('level', '').upper() == 'ERROR']
                for log in error_logs[-5:]:  # Show last 5 errors
                    timestamp = log.get('timestamp', '')
                    if isinstance(timestamp, datetime):
                        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    st.error(f"{timestamp} - {log.get('message', '')}")
            
            # Display recent warnings
            if warning_count > 0:
                st.subheader("Recent Warnings")
                warning_logs = [log for log in logs if log.get('level', '').upper() == 'WARNING']
                for log in warning_logs[-5:]:  # Show last 5 warnings
                    timestamp = log.get('timestamp', '')
                    if isinstance(timestamp, datetime):
                        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    st.warning(f"{timestamp} - {log.get('message', '')}")
            
            # Overall health status
            if error_rate > 0.1:  # More than 10% errors
                st.error("⚠️ Server Health: Critical")
            elif warning_rate > 0.2:  # More than 20% warnings
                st.warning("⚠️ Server Health: Warning")
            else:
                st.success("✅ Server Health: Good")
                
        except Exception as e:
            st.error(f"Error running health check: {str(e)}")
            self.logger.error(f"Health check error: {str(e)}")

    def execute_task(self, task_id: str):
        """Execute a task"""
        try:
            # Get task details
            task = self.agent_service.get_task(task_id)
            if not task:
                st.error("Task not found")
                return

            # Create a placeholder for progress updates
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            # Show initial progress
            progress_placeholder.progress(0)
            status_placeholder.text("Starting task execution...")
            
            # Execute task
            result = self.agent_service.execute_task(task_id)
            
            if result.get('status') == 'success':
                progress_placeholder.progress(100)
                status_placeholder.text("Task completed successfully!")
                st.success("Task completed successfully!")
                
                # Force refresh the task history
                st.session_state['task_history'] = self.agent_service.get_task_history()
                
                # Force a rerun to update the UI
                st.rerun()
            else:
                progress_placeholder.progress(0)
                status_placeholder.text("Task failed!")
                st.error(f"Task failed: {result.get('error', 'Unknown error')}")
            
        except Exception as e:
            st.error(f"Error executing task: {str(e)}")
            self.logger.error(f"Task execution error: {str(e)}")

    async def create_task(self, description: str, context: Dict[str, Any] = None):
        """Create a new task"""
        try:
            # Create task
            task = await self.agent_service.create_task(description, context)
            
            # Add to active tasks
            self.active_tasks.append(task)
            
            # Show success message
            st.success(f"Task created successfully! Task ID: {task['task_id']}")
            
            # Refresh the display
            st.rerun()
            
        except Exception as e:
            st.error(f"Error creating task: {str(e)}")
            self.logger.error(f"Task creation error: {str(e)}") 