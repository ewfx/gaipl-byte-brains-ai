from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import openai
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import logging
import asyncio
import pandas as pd
import numpy as np
from config.config import Config
from utils.openai_service import OpenAIService
from utils.log_service import LogService
import uuid

class AgentTask(BaseModel):
    """Model for agent tasks."""
    task_id: str
    description: str
    status: str = "pending"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    result: Optional[Dict[str, Any]] = None
    context: Dict[str, Any] = {}
    steps: List[Dict[str, Any]] = []

class AgentService:
    def __init__(self):
        """Initialize the Agent Service."""
        self.openai_service = OpenAIService()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Add console handler if not already added
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # Initialize task storage
        self.active_tasks = []
        self.task_history = []
        self._load_task_history()
        self._load_active_tasks()

    def _load_task_history(self):
        """Load task history from file"""
        try:
            # Get the absolute path to the task_history.json file
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            history_file = os.path.join(current_dir, "task_history.json")
            
            self.logger.info(f"Looking for task history file at: {history_file}")
            
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history_data = json.load(f)
                    # Convert string timestamps back to datetime objects
                    for task in history_data:
                        if 'created_at' in task:
                            task['created_at'] = datetime.fromisoformat(task['created_at'])
                        if 'completed_at' in task:
                            task['completed_at'] = datetime.fromisoformat(task['completed_at'])
                        if 'updated_at' in task:
                            task['updated_at'] = datetime.fromisoformat(task['updated_at'])
                    self.task_history = history_data
                    self.logger.info(f"Loaded {len(self.task_history)} tasks from history")
            else:
                self.logger.info("No task history file found, creating new file")
                self.task_history = []
                # Create the file if it doesn't exist
                with open(history_file, 'w') as f:
                    json.dump([], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error loading task history: {str(e)}")
            self.task_history = []

    def _save_task_history(self):
        """Save task history to file"""
        try:
            # Get the absolute path to the task_history.json file
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            history_file = os.path.join(current_dir, "task_history.json")
            
            self.logger.info(f"Saving task history to: {history_file}")
            
            # Convert datetime objects to ISO format strings for JSON serialization
            history_data = []
            for task in self.task_history:
                task_copy = task.copy()
                if 'created_at' in task_copy:
                    task_copy['created_at'] = task_copy['created_at'].isoformat()
                if 'completed_at' in task_copy:
                    task_copy['completed_at'] = task_copy['completed_at'].isoformat()
                if 'updated_at' in task_copy:
                    task_copy['updated_at'] = task_copy['updated_at'].isoformat()
                history_data.append(task_copy)
            
            with open(history_file, 'w') as f:
                json.dump(history_data, f, indent=2)
            self.logger.info(f"Saved {len(self.task_history)} tasks to history")
        except Exception as e:
            self.logger.error(f"Error saving task history: {str(e)}")

    def _load_active_tasks(self):
        """Load active tasks from file"""
        try:
            # Get the absolute path to the active_tasks.json file
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            tasks_file = os.path.join(current_dir, "active_tasks.json")
            
            self.logger.info(f"Looking for active tasks file at: {tasks_file}")
            
            if os.path.exists(tasks_file):
                try:
                    with open(tasks_file, 'r') as f:
                        tasks_data = json.load(f)
                        # Convert string timestamps back to datetime objects
                        for task in tasks_data:
                            if 'created_at' in task:
                                task['created_at'] = datetime.fromisoformat(task['created_at'])
                            if 'updated_at' in task:
                                task['updated_at'] = datetime.fromisoformat(task['updated_at'])
                        self.active_tasks = tasks_data
                        self.logger.info(f"Loaded {len(self.active_tasks)} active tasks")
                except json.JSONDecodeError:
                    self.logger.warning("Active tasks file is corrupted, creating new file")
                    self.active_tasks = []
                    # Backup the corrupted file
                    backup_file = tasks_file + '.bak'
                    if os.path.exists(tasks_file):
                        os.rename(tasks_file, backup_file)
                    # Create new empty file
                    with open(tasks_file, 'w') as f:
                        json.dump([], f, indent=2)
            else:
                self.logger.info("No active tasks file found, creating new file")
                self.active_tasks = []
                # Create the file if it doesn't exist
                with open(tasks_file, 'w') as f:
                    json.dump([], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error loading active tasks: {str(e)}")
            self.active_tasks = []

    def _save_active_tasks(self):
        """Save active tasks to file"""
        try:
            # Get the absolute path to the active_tasks.json file
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            tasks_file = os.path.join(current_dir, "active_tasks.json")
            
            self.logger.info(f"Saving active tasks to: {tasks_file}")
            
            # Convert datetime objects to ISO format strings for JSON serialization
            tasks_data = []
            for task in self.active_tasks:
                task_copy = task.copy()
                if 'created_at' in task_copy:
                    task_copy['created_at'] = task_copy['created_at'].isoformat()
                if 'updated_at' in task_copy:
                    task_copy['updated_at'] = task_copy['updated_at'].isoformat()
                if 'steps' in task_copy:
                    for step in task_copy['steps']:
                        if 'created_at' in step:
                            step['created_at'] = step['created_at'].isoformat()
                        if 'updated_at' in step:
                            step['updated_at'] = step['updated_at'].isoformat()
                tasks_data.append(task_copy)
            
            with open(tasks_file, 'w') as f:
                json.dump(tasks_data, f, indent=2)
            self.logger.info(f"Saved {len(self.active_tasks)} active tasks")
        except Exception as e:
            self.logger.error(f"Error saving active tasks: {str(e)}")
            raise

    async def _plan_task_steps(self, description: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Plan steps for a task"""
        try:
            # Create prompt for step planning
            prompt = f"""
            Task Description: {description}
            Context: {json.dumps(context or {})}
            
            Please plan the steps needed to complete this task. Each step should have:
            1. A unique ID (step_1, step_2, etc.)
            2. A description
            3. A type (analysis or action)
            4. Required parameters
            
            Return the steps as a JSON array without any markdown formatting.
            """
            
            # Get completion from OpenAI
            response = await self.openai_service.get_completion(prompt)
            
            # Clean the response by removing markdown code block markers if present
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            # Parse steps
            try:
                steps = json.loads(response)
            except json.JSONDecodeError:
                self.logger.error(f"Failed to parse steps from response: {response}")
                steps = []
            
            # Add status and timestamps to each step
            for i, step in enumerate(steps, 1):
                step["id"] = f"step_{i}"  # Ensure each step has a unique ID
                step["status"] = "pending"
                step["created_at"] = datetime.now()
                step["updated_at"] = datetime.now()
            
            return steps
            
        except Exception as e:
            self.logger.error(f"Error planning task steps: {str(e)}")
            return []

    async def create_task(self, description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new task"""
        try:
            # Generate task ID
            task_id = f"task_{len(self.active_tasks) + len(self.task_history) + 1}"
            
            # Plan task steps
            steps = await self._plan_task_steps(description, context)
            
            # Create task object
            task = {
                "task_id": task_id,
                "description": description,
                "context": context or {},
                "status": "pending",
                "steps": steps,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            # Add to active tasks
            self.active_tasks.append(task)
            
            # Save active tasks
            self._save_active_tasks()
            
            # Log task creation
            self.logger.info(f"Created new task: {task_id}")
            
            return task
            
        except Exception as e:
            self.logger.error(f"Error creating task: {str(e)}")
            raise

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get all active tasks"""
        return self.active_tasks

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID"""
        # Check active tasks first
        for task in self.active_tasks:
            if task["task_id"] == task_id:
                return task
        
        # Then check task history
        for task in self.task_history:
            if task["task_id"] == task_id:
                return task
        
        return None

    def get_task_history(self) -> List[Dict[str, Any]]:
        """Get task history"""
        self.logger.info(f"Retrieved {len(self.task_history)} tasks from history")
        return self.task_history

    def archive_task(self, task_id: str):
        """Archive a completed task"""
        try:
            # Find task in active tasks
            task = None
            for t in self.active_tasks:
                if t["task_id"] == task_id:
                    task = t
                    break
            
            if task:
                # Add completion timestamp
                task["completed_at"] = datetime.now()
                task["updated_at"] = datetime.now()
                
                # Move to history
                self.task_history.append(task)
                self.active_tasks.remove(task)
                
                # Save updated history and active tasks
                self._save_task_history()
                self._save_active_tasks()
                
                self.logger.info(f"Archived task: {task_id}")
            else:
                self.logger.warning(f"Task not found: {task_id}")
                
        except Exception as e:
            self.logger.error(f"Error archiving task: {str(e)}")
            raise

    def update_task_status(self, task_id: str, status: str):
        """Update task status"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = status
            self.active_tasks[task_id]["updated_at"] = datetime.now()

    def update_step_status(self, task_id: str, step_id: str, status: str):
        """Update step status"""
        if task_id in self.active_tasks:
            for step in self.active_tasks[task_id]["steps"]:
                if step["id"] == step_id:
                    step["status"] = status
                    step["updated_at"] = datetime.now()
                    break

    def execute_step(self, task_id: str, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step"""
        try:
            # Get task context
            task = self.get_task(task_id)
            if not task:
                return {"status": "error", "error": "Task not found"}

            # Execute step based on type
            step_type = step.get("type", "unknown")
            if step_type == "analysis":
                result = self._execute_analysis_step(step, task["context"])
            elif step_type == "action":
                result = self._execute_action_step(step, task["context"])
            else:
                result = {"status": "error", "error": f"Unknown step type: {step_type}"}

            # Update step result
            step["result"] = result
            step["status"] = result.get("status", "failed")
            step["updated_at"] = datetime.now()

            return result

        except Exception as e:
            self.logger.error(f"Error executing step: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _execute_analysis_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an analysis step"""
        try:
            # Create analysis prompt
            prompt = f"""
            Step Description: {step.get('description', '')}
            Context: {json.dumps(context)}
            
            Please analyze the given information and provide insights.
            """
            
            # Get completion from OpenAI
            response = self.openai_service.get_completion(prompt)
            
            return {
                "status": "success",
                "result": response
            }
            
        except Exception as e:
            self.logger.error(f"Error executing analysis step: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _execute_action_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action step"""
        try:
            # Create action prompt
            prompt = f"""
            Step Description: {step.get('description', '')}
            Context: {json.dumps(context)}
            
            Please execute the requested action and provide the result.
            """
            
            # Get completion from OpenAI
            response = self.openai_service.get_completion(prompt)
            
            return {
                "status": "success",
                "result": response
            }
            
        except Exception as e:
            self.logger.error(f"Error executing action step: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a task and return the result"""
        try:
            # Get task details
            task = self.get_task(task_id)
            if not task:
                return {"status": "error", "error": "Task not found"}

            # Update task status to running
            self.update_task_status(task_id, "running")
            
            # Execute each step
            steps = task.get('steps', [])
            for step in steps:
                # Execute step
                result = self.execute_step(task_id, step)
                
                # Update step status
                if result.get('status') == 'success':
                    self.update_step_status(task_id, step['id'], 'completed')
                else:
                    self.update_step_status(task_id, step['id'], 'failed')
                    self.update_task_status(task_id, "failed")
                    return result
            
            # Update task status to completed
            self.update_task_status(task_id, "completed")
            
            # Archive the completed task
            self.archive_task(task_id)
            
            # Log the task completion
            self.logger.info(f"Task {task_id} completed successfully and archived")
            
            return {
                "status": "success",
                "task_id": task_id,
                "message": "Task completed successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Error executing task: {str(e)}")
            self.update_task_status(task_id, "failed")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_task_status(self, task_id: str) -> AgentTask:
        """Get the current status of a task."""
        if task_id not in self.active_tasks:
            raise ValueError(f"Task {task_id} not found")
        return self.active_tasks[task_id]
    
    async def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute a single step of the task."""
        prompt = f"""
        Execute the following step:
        Step Name: {step['name']}
        Description: {step['description']}
        Action: {step['action']}
        Parameters: {json.dumps(step['parameters'], indent=2)}
        
        Context:
        {json.dumps(context, indent=2)}
        
        Provide the execution result in a structured format.
        """
        
        response = await self.openai_service.get_completion(prompt)
        
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {"error": "Failed to parse result", "raw_response": response}
    
    async def analyze_logs(self, prompt: str, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze logs using OpenAI
        Args:
            prompt: Analysis prompt
            logs: List of log entries
        Returns:
            Dict containing analysis results
        """
        try:
            # Prepare log data for analysis
            log_data = [
                {
                    "timestamp": log.get("timestamp", "").isoformat() if isinstance(log.get("timestamp"), datetime) else log.get("timestamp", ""),
                    "level": log.get("level", ""),
                    "message": log.get("message", ""),
                    "component": log.get("component", ""),
                    "server": log.get("server", ""),
                    "duration_ms": log.get("duration_ms", 0),
                    "status_code": log.get("status_code", 0)
                }
                for log in logs
            ]
            
            # Create analysis prompt
            analysis_prompt = f"""
            Analyze the following logs and provide insights:
            
            Log Summary:
            - Total entries: {len(logs)}
            - Time range: {logs[0]['timestamp'].isoformat() if isinstance(logs[0]['timestamp'], datetime) else logs[0]['timestamp']} to {logs[-1]['timestamp'].isoformat() if isinstance(logs[-1]['timestamp'], datetime) else logs[-1]['timestamp']}
            
            {prompt}
            
            Log Data:
            {json.dumps(log_data, indent=2)}
            
            Please provide:
            1. Summary of key events
            2. Potential issues or anomalies
            3. Recommendations for improvement
            
            Format your response as a JSON object with the following structure:
            {{
                "summary": "Overall summary of the analysis",
                "key_events": ["List of key events"],
                "issues": ["List of potential issues"],
                "recommendations": ["List of recommendations"]
            }}
            """
            
            # Get analysis from OpenAI
            response = await self.openai_service.get_completion(analysis_prompt)
            
            try:
                # Parse the response as JSON
                analysis = json.loads(response)
                
                # Add timestamp to the analysis
                analysis['timestamp'] = datetime.now().isoformat()
                
                return analysis
                
            except json.JSONDecodeError:
                # If response is not valid JSON, format it as a structured response
                return {
                    'summary': response,
                    'key_events': [],
                    'issues': [],
                    'recommendations': [],
                    'timestamp': datetime.now().isoformat()
                }
            
        except Exception as e:
            self.logger.error(f"Error analyzing logs: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_log_statistics(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate basic statistics from logs
        Args:
            logs: List of log entries
        Returns:
            Dict containing statistics
        """
        try:
            # Convert logs to DataFrame
            df = pd.DataFrame(logs)
            
            # Calculate statistics
            stats = {
                'total_logs': len(logs),
                'log_levels': df['level'].value_counts().to_dict(),
                'time_range': {
                    'start': df['timestamp'].min(),
                    'end': df['timestamp'].max()
                },
                'unique_components': df['component'].nunique(),
                'error_rate': len(df[df['level'] == 'ERROR']) / len(df) if len(df) > 0 else 0
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error calculating log statistics: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def detect_anomalies(self, prompt: str, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in logs using AI"""
        try:
            # Prepare log data for analysis
            log_data = [
                {
                    "timestamp": log.get("timestamp", "").isoformat() if isinstance(log.get("timestamp"), datetime) else log.get("timestamp", ""),
                    "level": log.get("level", ""),
                    "message": log.get("message", ""),
                    "component": log.get("component", ""),
                    "server": log.get("server", ""),
                    "duration_ms": log.get("duration_ms", 0),
                    "status_code": log.get("status_code", 0)
                }
                for log in logs
            ]
            
            # Create analysis prompt
            analysis_prompt = f"""
            Analyze the following logs for anomalies:
            
            Log Summary:
            - Total entries: {len(logs)}
            - Time range: {logs[0]['timestamp'].isoformat() if isinstance(logs[0]['timestamp'], datetime) else logs[0]['timestamp']} to {logs[-1]['timestamp'].isoformat() if isinstance(logs[-1]['timestamp'], datetime) else logs[-1]['timestamp']}
            
            {prompt}
            
            Log Data:
            {json.dumps(log_data, indent=2)}
            
            Please identify and describe any anomalies in the logs, including:
            1. Unusual patterns or spikes
            2. Unexpected error rates
            3. Performance anomalies
            4. Security concerns
            
            Format your response as a JSON array of anomalies, where each anomaly has:
            - type: The type of anomaly (error, performance, security, etc.)
            - description: A detailed description of the anomaly
            - severity: The severity level (low, medium, high)
            - affected_components: List of affected components
            - recommendations: List of recommendations to address the anomaly
            """
            
            # Get AI analysis
            response = await self.openai_service.get_completion(analysis_prompt)
            
            try:
                # Parse the response as JSON
                anomalies = json.loads(response)
                
                # Ensure each anomaly has a timestamp
                for anomaly in anomalies:
                    if 'timestamp' not in anomaly:
                        anomaly['timestamp'] = datetime.now().isoformat()
                
                return anomalies
                
            except json.JSONDecodeError:
                # If response is not valid JSON, format it as a single anomaly
                return [{
                    'type': 'error',
                    'description': f"Error parsing AI response: {response}",
                    'severity': 'high',
                    'affected_components': ['system'],
                    'recommendations': ['Check AI service configuration'],
                    'timestamp': datetime.now().isoformat()
                }]
                
        except Exception as e:
            self.logger.error(f"Error in anomaly detection: {str(e)}")
            return [{
                'type': 'error',
                'description': f"Error in anomaly detection: {str(e)}",
                'severity': 'high',
                'affected_components': ['system'],
                'recommendations': ['Check system logs for more details'],
                'timestamp': datetime.now().isoformat()
            }]

    async def generate_insights(self, prompt: str, logs: List[Dict]) -> str:
        """Generate insights from logs using AI"""
        try:
            # Create a structured prompt for insight generation
            system_prompt = """You are an expert in log analysis and system monitoring. Generate actionable insights
            from the provided logs. Focus on system health, performance, security, and user behavior patterns."""
            
            # Format logs for analysis
            log_summary = self._format_logs_for_analysis(logs)
            
            # Get analysis from OpenAI
            response = await self.openai_service.get_completion(
                f"{prompt}\n\nLog Data:\n{log_summary}",
                system_prompt=system_prompt
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {str(e)}")
            return f"Error generating insights: {str(e)}"
            
    def _format_logs_for_analysis(self, logs: List[Dict]) -> str:
        """Format logs for AI analysis"""
        if not logs:
            return "No logs available for analysis."
            
        # Create a summary of log statistics
        log_levels = {}
        status_codes = {}
        avg_response_time = 0
        total_requests = len(logs)
        
        for log in logs:
            # Count log levels
            level = log.get('level', 'UNKNOWN')
            log_levels[level] = log_levels.get(level, 0) + 1
            
            # Count status codes
            status = log.get('status_code')
            if status:
                status_codes[status] = status_codes.get(status, 0) + 1
                
            # Calculate average response time
            duration = log.get('duration_ms', 0)
            avg_response_time += duration
            
        avg_response_time = avg_response_time / total_requests if total_requests > 0 else 0
        
        # Format the summary
        summary = f"""
        Log Statistics:
        - Total entries: {total_requests}
        - Time range: {logs[0]['timestamp']} to {logs[-1]['timestamp']}
        
        Log Levels:
        {json.dumps(log_levels, indent=2)}
        
        Status Codes:
        {json.dumps(status_codes, indent=2)}
        
        Performance:
        - Average response time: {avg_response_time:.2f}ms
        
        Sample Log Messages:
        """
        
        # Add sample log messages
        for log in logs[:5]:  # Include first 5 logs as examples
            summary += f"\n- [{log['timestamp']}] {log['level']}: {log['message']}"
            
        return summary 