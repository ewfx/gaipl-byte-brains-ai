from typing import Dict, List, Any, Optional
from ..agent import IPEAgent
from ..executors import WorkflowExecutor, ExecutionResult
import os
from dotenv import load_dotenv

class IPEService:
    def __init__(self):
        """Initialize the IPE service."""
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.agent = IPEAgent(api_key=self.api_key)
        self.workflow_executor = WorkflowExecutor()
        self.active_processes: Dict[str, Dict[str, Any]] = {}
    
    def create_process(self, task_description: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new process plan for a task."""
        try:
            steps = self.agent.plan_process(task_description)
            process_id = f"process_{len(self.active_processes) + 1}"
            
            if parameters:
                for step in steps:
                    if step.name in parameters:
                        step.parameters.update(parameters[step.name])
            
            self.active_processes[process_id] = {
                "steps": steps,
                "status": "planned",
                "results": {}
            }
            
            return {
                "process_id": process_id,
                "steps": steps,
                "status": "planned"
            }
        except Exception as e:
            raise Exception(f"Error creating process: {str(e)}")
    
    def execute_process(self, process_id: str, step_name: Optional[str] = None) -> Dict[str, Any]:
        """Execute a process or a specific step."""
        if process_id not in self.active_processes:
            raise ValueError(f"Process {process_id} not found")
        
        process = self.active_processes[process_id]
        
        try:
            if step_name:
                # Execute specific step
                step = next((s for s in process["steps"] if s.name == step_name), None)
                if not step:
                    raise ValueError(f"Step {step_name} not found")
                
                result = self.agent.execute_step(step)
                process["results"][step_name] = result
                return {step_name: result}
            else:
                # Execute entire process
                results = self.agent.execute_process()
                process["results"].update(results)
                process["status"] = "completed"
                return results
        except Exception as e:
            process["status"] = "failed"
            raise Exception(f"Error executing process: {str(e)}")
    
    def get_process_status(self, process_id: str) -> Dict[str, str]:
        """Get the status of a process."""
        if process_id not in self.active_processes:
            raise ValueError(f"Process {process_id} not found")
        
        process = self.active_processes[process_id]
        return {
            "process_status": process["status"],
            "steps": self.agent.get_process_status()
        }
    
    def get_knowledge_base(self, process_id: str) -> Dict[str, Any]:
        """Get the knowledge base for a process."""
        if process_id not in self.active_processes:
            raise ValueError(f"Process {process_id} not found")
        
        return self.agent.knowledge_base
    
    def get_active_processes(self) -> List[Dict[str, Any]]:
        """Get all active processes."""
        return [
            {
                "process_id": pid,
                "status": process["status"],
                "steps": len(process["steps"]),
                "completed_steps": len([s for s in process["steps"] if s.status == "completed"])
            }
            for pid, process in self.active_processes.items()
        ]
    
    def execute_workflow(self, workflow_config: Dict[str, Any]) -> ExecutionResult:
        """Execute a workflow using the workflow executor."""
        return self.workflow_executor.execute(workflow_config) 